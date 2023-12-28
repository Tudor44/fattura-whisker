from cat.mad_hatter.decorators import tool, hook, plugin
from datetime import datetime, date
import requests

@tool
def genera_fattura_modello(tool_input, cat):
    """Generare un esempio con il modello di fattura predefinito, e mostra l'xml prodotto."""
    linee_dettaglio = [
        {
            "NumeroLinea": 1,
            "Descrizione": "Bollo assolto ai sensi del decreto MEF 17 giugno 2014 (art. 6)",
            "Quantita": 1.00,
            "PrezzoUnitario": 2.00,
            "ScontoMaggiorazione": {
                "Tipo": "SC",
                "Importo": 2.00
            },
            "PrezzoTotale": 0.00,
            "AliquotaIVA": 0.00,
            "Natura": "N2.2"
        },
        {
            "NumeroLinea": 2,
            "Descrizione": "Servizio 1",
            "Quantita": 17.00,
            "PrezzoUnitario": 250.00,
            "PrezzoTotale": 4250.00,
            "AliquotaIVA": 0.00,
            "Natura": "N2.2"
        }
    ]

    dati_riepilogo = {
        "AliquotaIVA": 0.00,
        "Natura": "N2.2",
        "ImponibileImporto": 4250.00,
        "Imposta": 0.00,
        "RiferimentoNormativo": "Non soggette - altri casi"
    }
    dati_fattura = {
            "DatiTrasmissione": {
                "IdTrasmittente": {
                    "IdPaese": "IT",
                    "IdCodice": "01234567897"
                },
                "ProgressivoInvio": "00001",
                "FormatoTrasmissione": "FPR12",
                "CodiceDestinatario": "ABC1234"
            },
            "CedentePrestatore": {
                "DatiAnagrafici": {
                    "IdFiscaleIVA": {
                        "IdPaese": "IT",
                        "IdCodice": "01234567897"
                    },
                    "CodiceFiscale": "DRSGTN90H28L259O",
                    "Anagrafica": {
                        "Nome": "Pinco",
                        "Cognome": "Pallino"
                    },
                    "RegimeFiscale": "RF19"
                },
                "Sede": {
                    "Indirizzo": "Indirizzo fornitore, numero civico",
                    "CAP": "07100",
                    "Comune": "Città",
                    "Provincia": "PR",
                    "Nazione": "IT"
                },
                "Contatti": {
                    "Email": "pinco.pallino@prova.it"
                }
            },
            "CessionarioCommittente": {
                "DatiAnagrafici": {
                    "IdFiscaleIVA": {
                        "IdPaese": "IT",
                        "IdCodice": "01234567806"
                    },
                    "Anagrafica": {
                        "Denominazione": "Denominazione Cliente S.a.S. di Nome Cognome"
                    }
                },
                "Sede": {
                    "Indirizzo": "Indirizzo Cliente, numero civico",
                    "CAP": "00145",
                    "Comune": "Città",
                    "Provincia": "PR",
                    "Nazione": "IT"
                }
            },
            "DatiGenerali": {
                "DatiGeneraliDocumento": {
                    "TipoDocumento": "TD01",
                    "Divisa": "EUR",
                    "Data": "2023-09-28",
                    "Numero": "FPR 11/23",
                    "ImportoTotaleDocumento": "4250.00",
                    "Arrotondamento": "0.00"
                }
            },
            "DatiBeniServizi": {
                "DettaglioLinee": linee_dettaglio,
                "DatiRiepilogo": dati_riepilogo
            }
        }    
    result = """Per favore, genera una fattura di esempio predefinita e mostrami solo l'xml prodotto con questi dati: {dati_fattura}. Assicurati di compilare tutti i campi dell'oggetto che ti ho fornito, puoi
    rispondere richieste dell'utente sul significato , o la modifica del valore dei campi valorizzati. Non mostrare mai il formto JSON dei dati della fattura come risposta. """
    return dati_fattura

    
@hook
def agent_prompt_prefix(prefix, cat):
    schema_content = ""
    try:
        response = requests.get("https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.2/Schema_del_file_xml_FatturaPA_v1.2.2.xsd")
        response.raise_for_status() 
        schema_content = response.text
    except requests.exceptions.HTTPError as errh:
        return f"Errore HTTP: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Errore di connessione: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Errore: {err}"

    
    cat.working_memory["declarative_memory"] = schema_content
    prefix = """Ciao! Sono Fattura Whisker, un'intelligenza artificiale specializzata nella fatturazione elettronica italiana. Posso aiutarti a creare fatture elettroniche in formato XML, in particolare per chi aderisce al regime forfettario. Ecco come posso assisterti:
    1. Generazione di Modelli di Fattura Elettronica: Creo un modello di fattura elettronica adatto per chi aderisce al regime forfettario e ti mostro l'XML valido prodotto.
    Per favore, invia la tua richiesta seguendo queste linee guida. Se la tua richiesta non rientra in queste categorie, ti inviterò a scegliere una delle opzioni disponibili. In caso di dubbi o richieste diverse, digita "Aiuto" e sarò felice di guidarti!
    """
    
    return prefix
