(function ($) {
    'use strict';

    if (window.missioneInitialized) {
        return;
    }
    window.missioneInitialized = true;

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

    function initializeMissionId() {
        const path = window.location.pathname;

        let matches = path.match(/\/missione\/(\d+)\//);
        if (!matches) {
            matches = path.match(/\/missione\/(\d+)$/);
        }
        if (!matches) {
            matches = path.match(/\/(\d+)\/$/);
        }

        if (matches) {
            CONFIG.missionId = matches[1];
        } else {
            console.error('Could not extract mission ID from URL:', path);
            const missionElement = document.querySelector('[data-mission-id]');
            if (missionElement) {
                CONFIG.missionId = missionElement.getAttribute('data-mission-id');
            }
        }
    }

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

    function hasCardData(card) {
        const inputs = card.find('input, select, textarea').not('[type="hidden"]').not('[name$="-DELETE"]').not('[name$="-id"]');
        let hasData = false;

        inputs.each(function() {
            const $input = $(this);
            const value = $input.val();
            const type = $input.attr('type');

            if (type === 'file') {
                if ($input[0].files && $input[0].files[0]) {
                    hasData = true;
                    return false;
                }
                return true;
            }

            if (value && value.trim() !== '' && value !== '0' && value !== '0.0') {
                hasData = true;
                return false;
            }
        });

        return hasData;
    }

    function getCardInfo(card) {
        if (!card || card.length === 0) {
            console.error('getCardInfo: No card provided');
            return { section: null, cardId: null };
        }

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

        let idField = card.find('[name$="-id"]');
        let cardId = null;

        if (idField.length > 0) {
            cardId = idField.val();
        } else {
            const patterns = [
                `input[name*="${section}"][name$="-id"]`,
                `input[name*="${section.toLowerCase()}"][name$="-id"]`,
                `input[name*="${section}_set"][name$="-id"]`,
                `input[name*="${section.toLowerCase()}_set"][name$="-id"]`,
                `input[name*="${section.slice(0, -1)}_set"][name$="-id"]`,
                `input[name^="form-"][name$="-id"]`,
                'input[name$="-id"]'
            ];

            for (const pattern of patterns) {
                idField = card.find(pattern);
                if (idField.length > 0) {
                    cardId = idField.val();
                    break;
                }
            }
        }

        if (cardId && (cardId === '' || cardId === 'undefined' || cardId === 'null')) {
            cardId = null;
        }

        return { section, cardId };
    }

    function serializeCard(card) {
        const data = new FormData();
        const inputs = card.find('input, select, textarea');

        inputs.each(function() {
            const $input = $(this);
            const name = $input.attr('name');
            const type = $input.attr('type');

            if (!name) return;

            let cleanName = name;

            let prefixMatch = name.match(/^[a-z]+-\d+-(.+)$/);
            if (prefixMatch) {
                cleanName = prefixMatch[1];
            } else {
                prefixMatch = name.match(/^[a-z]+_set-\d+-(.+)$/);
                if (prefixMatch) {
                    cleanName = prefixMatch[1];
                } else {
                    prefixMatch = name.match(/^form-\d+-(.+)$/);
                    if (prefixMatch) {
                        cleanName = prefixMatch[1];
                    } else {
                        if (name.includes('TOTAL_FORMS') || name.includes('INITIAL_FORMS') || name.includes('MAX_NUM_FORMS')) {
                            cleanName = name;
                        } else {
                            console.log(`DEBUG serializeCard Pattern 5 (no-match): ${name} -> ${cleanName}`);
                        }
                    }
                }
            }

            if (type === 'file') {
                if ($input[0].files && $input[0].files[0]) {
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

        data.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        data.append('mission_id', CONFIG.missionId);

        return data;
    }

    function saveCard(card) {
        const { section, cardId } = getCardInfo(card);

        if (!CONFIG.missionId) {
            setCardState(card, 'error');
            return;
        }

        if (!section) {
            return;
        }

        if (!hasCardData(card)) {
            return;
        }

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
                    
                }
            }
        });
    }

    function deleteCard(card) {
        const { section, cardId } = getCardInfo(card);

        if (!CONFIG.missionId) {
            console.error('Mission ID not found - cannot delete card');
            setCardState(card, 'error');
            return;
        }

        if (!section) {
            console.error('Section not found - cannot delete card');
            setCardState(card, 'error');
            return;
        }

        if (!cardId) {
            card.fadeOut(300, function() {
                $(this).remove();
            });
            return;
        }

        setCardState(card, 'saving');

        const endpoint = CONFIG.endpoints[section];
        if (!endpoint) {
            console.error(`No endpoint found for section: ${section}`);
            setCardState(card, 'error');
            return;
        }

        const url = endpoint + cardId + '/delete/';

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
                    
                }
            }
        });
    }

    function cleanupFormsetDeleteLinks() {
        $('.formset-card').each(function() {
            const card = $(this);
            const existingDeleteLinks = card.find('a').filter(function() {
                const $this = $(this);
                return $this.text().includes('Elimina') && !$this.hasClass('delete');
            });

            if (existingDeleteLinks.length > 0) {
                existingDeleteLinks.remove();
            }
        });
    }

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

        $(document).on('input change', '.formset-card input, .formset-card select, .formset-card textarea', function() {
            const card = $(this).closest('.formset-card');
            if (card.length === 0) return;

            if (card.hasClass('card-error')) {
                setCardState(card, 'unsaved');
            }

            debouncedSaveCard(card);
        });

        $(document).on('change', '.formset-card input[type="file"]', function() {
            const card = $(this).closest('.formset-card');
            if (card.length === 0) return;

            const fileName = this.files && this.files[0] ? this.files[0].name : 'No file';

            if (card.hasClass('card-error')) {
                setCardState(card, 'unsaved');
            }

            saveCard(card);
        });

        $(document).on('click', '.delete', function(e) {
            e.preventDefault();
            e.stopImmediatePropagation();

            const card = $(this).closest('.formset-card');
            if (card.length === 0) {
                console.error('Delete button click: No .formset-card found');
                return;
            }

            if (card.hasClass('card-saving')) {
                return;
            }

            deleteCard(card);
        });

        $('.formset-card').each(function() {
            setCardState($(this), 'unsaved');
            addCustomDeleteButton($(this).closest('.pasti_formset_row, .pernottamenti_formset_row, .trasporti_formset_row, .convegni_formset_row, .altrespese_formset_row'));
        });
    }

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

            $(config.row).formset({
                prefix: prefix,
                addText: 'Aggiungi',
                deleteText: 'Elimina',
                ifdelete: false,
                added: function(row) {
                    const card = $(row).find('.formset-card').length > 0 ? $(row).find('.formset-card') : $(row);
                    setCardState(card, 'unsaved');

                    addCustomDeleteButton(row);
                },
                removed: function(row) {}
            });
        });
    }

    function addCustomDeleteButton(row) {
        if (row.find('.delete').length > 0) {
            return;
        }

        const deleteButton = $('<a class="delete btn btn-danger" href="javascript:void(0)">Elimina</a>');
        const deleteContainer = $('<div class="mx-1" style="margin-top: 28px"></div>');
        deleteContainer.append(deleteButton);

        const cardBody = row.find('.card-body');
        if (cardBody.length > 0) {
            cardBody.append(deleteContainer);
        } else {
            row.append(deleteContainer);
        }
    }

    $(document).ready(function() {
        initializeMissionId();
        cleanupFormsetDeleteLinks();
        initializeCards();
        initializeFormsets();
    });

})(jQuery);