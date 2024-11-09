// ==UserScript==
// @name         Autocompilatore richieste kasko
// @namespace    https://github.com/prittt/missioni-unimore
// @version      0.1
// @supportURL   https://github.com/prittt/missioni-unimore/issues
// @downloadURL  https://github.com/prittt/missioni-unimore/raw/master/autocompilatore_richieste_kasko.user.js
// @description  Compilazione automatica del form per le richieste kasko
// @author       Costantino Grana
// @match        https://wtr.unimore.it/private/kasko/Richiesta.aspx
// @match        https://missioni.ing.unimore.it/resoconto/*
// @grant        GM_setValue
// @grant        GM_getValue
// ==/UserScript==

function autofill() {
    var data_richiesta =		document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor9" ); // Data richiesta
    var autorizzato_da =		document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor10_I"); // Autorizzato da
    var luogo_missione =		document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor11_I"); // Luogo missione
    var km_percorsi =			document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor12_I"); // Km percorsi
    var data_inizio_missione =	document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor13_I"); // Data inizio missione
    var data_fine_missione =	document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor14_I"); // Data fine missione
    var durata =				document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor16_I"); // Durata
    var unita_di_misura =		document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor18_I"); // Unità di misura
    var marca_mezzo =			document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor19_I"); // Marca mezzo
    var tipo_mezzo =			document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor20_I"); // Tipo mezzo
    var targa =					document.getElementById("ctl00_ContentPlaceHolder1_gvRichieste_efnew_pageControl_DXEditor21_I"); // Targa

    let event = new KeyboardEvent('focus');

    data_richiesta.value = GM_getValue("data_richiesta");
    data_richiesta.dispatchEvent(event)
    autorizzato_da.value = GM_getValue("autorizzato_da");
    luogo_missione.value = GM_getValue("luogo_missione");
    km_percorsi.value = GM_getValue("km_percorsi");
    data_inizio_missione.value = GM_getValue("data_inizio_missione");
    data_inizio_missione.dispatchEvent(event)
    data_fine_missione.value = GM_getValue("data_fine_missione");
    data_fine_missione.dispatchEvent(event)
    durata.value = GM_getValue("durata");
    unita_di_misura.value = GM_getValue("unita_di_misura");
    marca_mezzo.value = GM_getValue("marca_mezzo");
    tipo_mezzo.value = GM_getValue("tipo_mezzo");
    targa.value = GM_getValue("targa");
}

(function() {
    'use strict';

    if (window.location.hostname == "wtr.unimore.it") {
        if (GM_getValue("data_richiesta","invalid") != "invalid") {
            var button = document.createElement("input");
            button.type = "button";
            button.value = "Auto fill with data from Tampermonkey storage";
            button.onclick = autofill;
            document.getElementsByTagName("body")[0].getElementsByTagName("div")[2].getElementsByTagName("div")[1].appendChild(button);
        }
    }
    else {
        GM_setValue("data_richiesta",document.getElementById("data_richiesta").innerText);
        GM_setValue("autorizzato_da",document.getElementById("autorizzato_da").innerText);
        GM_setValue("luogo_missione",document.getElementById("luogo_missione").innerText);
        GM_setValue("km_percorsi",document.getElementById("km_percorsi").innerText);
        GM_setValue("data_inizio_missione",document.getElementById("data_inizio_missione").innerText);
        GM_setValue("data_fine_missione",document.getElementById("data_fine_missione").innerText);
        GM_setValue("durata",document.getElementById("durata").innerText);
        GM_setValue("unita_di_misura",document.getElementById("unita_di_misura").innerText);
        GM_setValue("marca_mezzo",document.getElementById("marca_mezzo").innerText);
        GM_setValue("tipo_mezzo",document.getElementById("tipo_mezzo").innerText);
        GM_setValue("targa",document.getElementById("targa").innerText);
    }

})();
