/* static/RimborsiApp/js/missione.js - Per-Card Save/Delete System */
(function ($) {
    'use strict';

    // Prevent multiple initialization
    if (window.missioneInitialized) {
        return;
    }
    window.missioneInitialized = true;

    // Configuration
    const CONFIG = {
        debounceDelay: 3000,
        missionId: null,
        endpoints: {
            pasti: '/save-pasto/',
            pernottamenti: '/save-pernottamento/',
            trasporti: '/save-trasporto/',
            convegni: '/save-convegno/',
            altrespese: '/save-altrespesa/'
        }
    };

    // Initialize mission ID from URL
    function initializeMissionId() {
        const path = window.location.pathname;
        console.log('Current path:', path);

        // Try multiple patterns
        let matches = path.match(/\/missione\/(\d+)\//);
        if (!matches) {
            matches = path.match(/\/missione\/(\d+)$/);
        }
        if (!matches) {
            matches = path.match(/\/(\d+)\/$/);
        }

        if (matches) {
            CONFIG.missionId = matches[1];
            console.log('Mission ID found:', CONFIG.missionId);
        } else {
            console.error('Could not extract mission ID from URL:', path);
            // Try to get from a hidden field or data attribute as fallback
            const missionElement = document.querySelector('[data-mission-id]');
            if (missionElement) {
                CONFIG.missionId = missionElement.getAttribute('data-mission-id');
                console.log('Mission ID from data attribute:', CONFIG.missionId);
            }
        }
    }

    // Utility functions
    function debounce(func, delay) {
        let timeout;
        return function (...args) {
            const context = this;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), delay);
        };
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Card state management
    function setCardState(card, state) {
        card.removeClass('card-unsaved card-saved card-error card-saving border-left-warning border-left-success border-left-danger');
        card.css('transition', 'background-color 0.5s ease');

        switch(state) {
            case 'saving':
                card.addClass('card-saving border-left-warning');
                break;
            case 'saved':
                card.addClass('card-saved border-left-success');
                break;
            case 'error':
                card.addClass('card-error border-left-danger');
                break;
            case 'unsaved':
            default:
                card.addClass('card-unsaved');
                break;
        }
    }

    // Check if card has meaningful data
    function hasCardData(card) {
        const inputs = card.find('input, select, textarea').not('[type="hidden"]').not('[name$="-DELETE"]').not('[name$="-id"]');
        let hasData = false;

        inputs.each(function() {
            const $input = $(this);
            const value = $input.val();
            const type = $input.attr('type');

            // Special handling for file inputs
            if (type === 'file') {
                if ($input[0].files && $input[0].files[0]) {
                    console.log(`hasCardData: Found file ${$input[0].files[0].name}`);
                    hasData = true;
                    return false; // break
                }
                return true; // continue to next input
            }

            // Check for meaningful content in other inputs
            if (value && value.trim() !== '' && value !== '0' && value !== '0.0') {
                hasData = true;
                return false; // break
            }
        });

        console.log(`hasCardData result: ${hasData}`);
        return hasData;
    }

    // Get card section and ID
    function getCardInfo(card) {
        // Ensure we have a valid card element
        if (!card || card.length === 0) {
            console.error('getCardInfo: No card provided');
            return { section: null, cardId: null };
        }

        // Find the form with data-section attribute
        const form = card.closest('form[data-section]');
        if (form.length === 0) {
            console.error('getCardInfo: No form with data-section found');
            return { section: null, cardId: null };
        }

        const section = form.data('section');
        if (!section) {
            console.error('getCardInfo: No section data found on form');
            return { section: null, cardId: null };
        }

        // Find the ID field - try multiple approaches for different formset patterns
        let idField = card.find('[name$="-id"]');
        let cardId = null;

        if (idField.length > 0) {
            cardId = idField.val();
            console.log(`getCardInfo: Found ID field with value: ${cardId}`);
        } else {
            // Try to find by specific patterns for each section type
            const patterns = [
                // Pattern 1: Custom prefix for modelformsets (pernottamenti-0-id, convegni-1-id, altrespese-2-id)
                `input[name*="${section}"][name$="-id"]`,
                `input[name*="${section.toLowerCase()}"][name$="-id"]`,
                // Pattern 2: Default inline formset patterns (trasporti_set-0-id, pasti_set-1-id)
                `input[name*="${section}_set"][name$="-id"]`,
                `input[name*="${section.toLowerCase()}_set"][name$="-id"]`,
                // Pattern 3: Singular forms (trasporto_set-0-id, pasto_set-1-id)
                `input[name*="${section.slice(0, -1)}_set"][name$="-id"]`, // Remove 's' from plural
                // Pattern 4: Default modelformset pattern (form-0-id)
                `input[name^="form-"][name$="-id"]`,
                // Pattern 5: Any ID field as fallback
                'input[name$="-id"]'
            ];

            for (const pattern of patterns) {
                idField = card.find(pattern);
                if (idField.length > 0) {
                    cardId = idField.val();
                    console.log(`getCardInfo: Found ID field using pattern ${pattern}, value: ${cardId}`);
                    break;
                }
            }
        }

        // Validate cardId
        if (cardId && (cardId === '' || cardId === 'undefined' || cardId === 'null')) {
            cardId = null;
        }

        console.log('DEBUG getCardInfo:', {
            section: section,
            cardId: cardId,
            idFieldLength: idField.length,
            idFieldValue: idField.length > 0 ? idField.val() : 'N/A',
            idFieldName: idField.length > 0 ? idField.attr('name') : 'N/A'
        });

        return { section, cardId };
    }

    // Serialize card data
    function serializeCard(card) {
        const data = new FormData();
        const inputs = card.find('input, select, textarea');

        inputs.each(function() {
            const $input = $(this);
            const name = $input.attr('name');
            const type = $input.attr('type');

            if (!name) return;

            // Extract clean field name by removing formset prefix
            // Handle multiple patterns:
            // 1. "pernottamenti-1-data" -> "data" (modelformset with custom prefix)
            // 2. "trasporti_set-0-data" -> "data" (inlineformset with default prefix)
            // 3. "pasti_set-0-importo1" -> "importo1" (inlineformset with default prefix)
            // 4. "form-0-data" -> "data" (modelformset with default prefix)
            let cleanName = name;

            // Pattern 1: custom_prefix-number-field (e.g., pernottamenti-1-data, convegni-0-importo, altrespese-2-descrizione)
            let prefixMatch = name.match(/^[a-z]+-\d+-(.+)$/);
            if (prefixMatch) {
                cleanName = prefixMatch[1];
                console.log(`DEBUG serializeCard Pattern 1: ${name} -> ${cleanName}`);
            } else {
                // Pattern 2: modelname_set-number-field (e.g., trasporti_set-0-data, pasti_set-1-importo1)
                prefixMatch = name.match(/^[a-z]+_set-\d+-(.+)$/);
                if (prefixMatch) {
                    cleanName = prefixMatch[1];
                    console.log(`DEBUG serializeCard Pattern 2: ${name} -> ${cleanName}`);
                } else {
                    // Pattern 3: form-number-field (e.g., form-0-data) - default modelformset prefix
                    prefixMatch = name.match(/^form-\d+-(.+)$/);
                    if (prefixMatch) {
                        cleanName = prefixMatch[1];
                        console.log(`DEBUG serializeCard Pattern 3: ${name} -> ${cleanName}`);
                    } else {
                        // Pattern 4: formset management form fields - keep as is
                        // (e.g., form-TOTAL_FORMS, form-INITIAL_FORMS, pernottamenti-TOTAL_FORMS)
                        if (name.includes('TOTAL_FORMS') || name.includes('INITIAL_FORMS') || name.includes('MAX_NUM_FORMS')) {
                            cleanName = name;
                            console.log(`DEBUG serializeCard Pattern 4 (management): ${name} -> ${cleanName}`);
                        } else {
                            // Pattern 5: no prefix recognized, use as-is (shouldn't happen in normal cases)
                            console.log(`DEBUG serializeCard Pattern 5 (no-match): ${name} -> ${cleanName}`);
                        }
                    }
                }
            }

            if (type === 'file') {
                if ($input[0].files && $input[0].files[0]) {
                    console.log(`DEBUG serializeCard FILE: Adding file ${cleanName} = ${$input[0].files[0].name}`);
                    data.append(cleanName, $input[0].files[0]);
                } else {
                    console.log(`DEBUG serializeCard FILE: No file selected for ${cleanName}`);
                }
            } else if (type === 'checkbox' || type === 'radio') {
                if ($input.is(':checked')) {
                    data.append(cleanName, $input.val());
                }
            } else {
                data.append(cleanName, $input.val());
            }
        });

        // Add CSRF token
        data.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        data.append('mission_id', CONFIG.missionId);

        return data;
    }

    // Save individual card
    function saveCard(card) {
        const { section, cardId } = getCardInfo(card);

        // Validate mission ID
        if (!CONFIG.missionId) {
            console.error('Mission ID not found - cannot save card');
            setCardState(card, 'error');
            return;
        }

        if (!section) {
            console.error('No section found for card');
            return;
        }

        // Skip if card has no meaningful data
        if (!hasCardData(card)) {
            console.log(`Card has no data, skipping save`);
            return;
        }

        console.log(`Saving ${section} card with ID: ${cardId || 'new'}`);

        setCardState(card, 'saving');

        const endpoint = CONFIG.endpoints[section];
        if (!endpoint) {
            console.error(`No endpoint configured for section: ${section}`);
            setCardState(card, 'error');
            return;
        }

        const url = endpoint + (cardId ? cardId + '/' : '');
        const formData = serializeCard(card);

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.success) {
                    setCardState(card, 'saved');

                    // Update card ID if it was a new card
                    if (!cardId && response.id) {
                        const idField = card.find('[name$="-id"]');
                        idField.val(response.id);
                    }

                } else {
                    setCardState(card, 'error');
                }
            },
            error: function(xhr, errmsg, err) {
                setCardState(card, 'error');
                let error = 'Errore del server';
                try {
                    const response = JSON.parse(xhr.responseText);
                    error = response.error || error;
                } catch (e) {
                    // Use default error
                }
            }
        });
    }

    // Delete individual card
    function deleteCard(card) {
        // Extract card info FIRST, before any DOM manipulation
        const { section, cardId } = getCardInfo(card);

        console.log(`Attempting to delete ${section} card with ID: ${cardId}`);

        // Validate mission ID
        if (!CONFIG.missionId) {
            console.error('Mission ID not found - cannot delete card');
            setCardState(card, 'error');
            return;
        }

        // Validate section
        if (!section) {
            console.error('Section not found - cannot delete card');
            setCardState(card, 'error');
            return;
        }

        if (!cardId) {
            // New card that hasn't been saved yet, just remove from DOM
            console.log('Deleting unsaved card from DOM');
            card.fadeOut(300, function() {
                $(this).remove();
            });
            return;
        }

        console.log(`Deleting saved ${section} card with ID: ${cardId}`);

        setCardState(card, 'saving');

        const endpoint = CONFIG.endpoints[section];
        if (!endpoint) {
            console.error(`No endpoint found for section: ${section}`);
            setCardState(card, 'error');
            return;
        }

        const url = endpoint + cardId + '/delete/';

        console.log('DEBUG deleteCard:', {
            section: section,
            cardId: cardId,
            endpoint: endpoint,
            finalUrl: url,
            missionId: CONFIG.missionId
        });

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': getCookie('csrftoken'),
                'mission_id': CONFIG.missionId
            },
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                if (response.success) {
                    card.fadeOut(300, function() {
                        $(this).remove();
                    });
                } else {
                    setCardState(card, 'error');
                }
            },
            error: function(xhr, errmsg, err) {
                setCardState(card, 'error');
                let error = 'Errore del server';
                try {
                    const response = JSON.parse(xhr.responseText);
                    error = response.error || error;
                } catch (e) {
                    // Use default error
                }
            }
        });
    }

    // Clean up any existing formset delete links to prevent conflicts
    function cleanupFormsetDeleteLinks() {
        // Remove delete links that might have been added by the formset plugin
        $('.formset-card').each(function() {
            const card = $(this);
            const existingDeleteLinks = card.find('a').filter(function() {
                const $this = $(this);
                return $this.text().includes('Elimina') && !$this.hasClass('delete');
            });

            if (existingDeleteLinks.length > 0) {
                console.log('Removing existing formset delete links:', existingDeleteLinks.length);
                existingDeleteLinks.remove();
            }
        });
    }

    // Initialize autosave and delete functionality
    function initializeCards() {
        const cardTimeouts = new Map();
        function debouncedSaveCard(card) {
            const cardElement = card[0];
            if (cardTimeouts.has(cardElement)) {
                clearTimeout(cardTimeouts.get(cardElement));
            }

            const timeoutId = setTimeout(() => {
                saveCard(card);
                cardTimeouts.delete(cardElement);
            }, CONFIG.debounceDelay);
            
            cardTimeouts.set(cardElement, timeoutId);
        }

        // Handle input changes for autosave
        $(document).on('input change', '.formset-card input, .formset-card select, .formset-card textarea', function() {
            const card = $(this).closest('.formset-card');
            if (card.length === 0) return;

            // Clear error state when user modifies data
            if (card.hasClass('card-error')) {
                setCardState(card, 'unsaved');
            }

            debouncedSaveCard(card);
        });

        // Handle file uploads immediately (no debounce)
        $(document).on('change', '.formset-card input[type="file"]', function() {
            const card = $(this).closest('.formset-card');
            if (card.length === 0) return;

            const fileName = this.files && this.files[0] ? this.files[0].name : 'No file';
            console.log(`File upload detected: ${fileName}`);

            if (card.hasClass('card-error')) {
                setCardState(card, 'unsaved');
            }

            saveCard(card);
        });

        // Handle delete button clicks - use stopImmediatePropagation to prevent conflicts
        $(document).on('click', '.delete', function(e) {
            e.preventDefault();
            e.stopImmediatePropagation(); // Prevent other handlers from firing

            const card = $(this).closest('.formset-card');
            if (card.length === 0) {
                console.error('Delete button click: No .formset-card found');
                return;
            }

            // Prevent multiple clicks
            if (card.hasClass('card-saving')) {
                console.log('Delete button click: Card is already being saved, ignoring');
                return;
            }

            console.log('Delete button clicked, calling deleteCard');
            deleteCard(card);
        });

        // Set initial state for existing cards and ensure they have delete buttons
        $('.formset-card').each(function() {
            setCardState($(this), 'unsaved');
            // Ensure existing cards have proper delete buttons
            addCustomDeleteButton($(this).closest('.pasti_formset_row, .pernottamenti_formset_row, .trasporti_formset_row, .convegni_formset_row, .altrespese_formset_row'));
        });
    }

    // Initialize formsets (for adding new cards)
    function initializeFormsets() {
        const formsetConfigs = [
            { container: '#pasti-formset-container', row: '.pasti_formset_row' },
            { container: '#pernottamenti-formset-container', row: '.pernottamenti_formset_row' },
            { container: '#trasporti-formset-container', row: '.trasporti_formset_row' },
            { container: '#convegni-formset-container', row: '.convegni_formset_row' },
            { container: '#altrespese-formset-container', row: '.altrespese_formset_row' }
        ];

        formsetConfigs.forEach(config => {
            const container = $(config.container);
            if (container.length === 0) return;

            const prefix = container.data('prefix');
            if (!prefix) {
                console.warn(`No prefix found for ${config.container}`);
                return;
            }

            console.log(`Initializing formset: ${config.container}`);

            $(config.row).formset({
                prefix: prefix,
                addText: 'Aggiungi',
                deleteText: 'Elimina',
                ifdelete: false, // Disable built-in delete handling
                added: function(row) {
                    const card = $(row).find('.formset-card').length > 0 ? $(row).find('.formset-card') : $(row);
                    setCardState(card, 'unsaved');
                    console.log('Added new formset row');

                    // Add manual delete button since we disabled automatic delete
                    addCustomDeleteButton(row);
                },
                removed: function(row) {
                    // This should no longer be called due to ifdelete: false
                    console.log('Formset removed callback (should not fire)');
                }
            });
        });
    }

    // Add custom delete button to new rows
    function addCustomDeleteButton(row) {
        // Check if delete button already exists
        if (row.find('.delete').length > 0) {
            return;
        }

        const deleteButton = $('<a class="delete btn btn-danger" href="javascript:void(0)">Elimina</a>');
        const deleteContainer = $('<div class="mx-1" style="margin-top: 28px"></div>');
        deleteContainer.append(deleteButton);

        // Add the delete button to the card body
        const cardBody = row.find('.card-body');
        if (cardBody.length > 0) {
            cardBody.append(deleteContainer);
        } else {
            // Fallback: add to the row itself
            row.append(deleteContainer);
        }
    }

    // Initialize everything when document is ready
    $(document).ready(function() {
        console.log('Initializing Missione per-card system...');

        initializeMissionId();
        cleanupFormsetDeleteLinks(); // Clean up any existing conflicting delete links
        initializeCards();
        initializeFormsets();

        console.log('Missione per-card system initialized successfully');
    });

})(jQuery);