import pymcdm.methods as crisp_methods
import pyfdm.methods as fuzzy_methods
import numpy as np

mcda_methods = {
    'ARAS': {
        'crisp': crisp_methods.ARAS,
        'fuzzy': fuzzy_methods.fARAS
    },
    'COCOSO': {
        'crisp': crisp_methods.COCOSO
    },
    'CODAS': {
        'crisp': crisp_methods.CODAS,
        'fuzzy': fuzzy_methods.fCODAS
    },
    'COMET': {
        'crisp': crisp_methods.COMET
    },
    'COPRAS': {
        'crisp': crisp_methods.COPRAS,
        'fuzzy': fuzzy_methods.fCOPRAS
    },
    'EDAS': {
        'crisp': crisp_methods.EDAS,
        'fuzzy': fuzzy_methods.fEDAS
    },
    'ERVD': {
        'crisp': crisp_methods.ERVD,
    },
    'INPUT': {},
    'MABAC': {
        'crisp': crisp_methods.MABAC,
        'fuzzy': fuzzy_methods.fMABAC
    },
    'MAIRCA': {
        'crisp': crisp_methods.MAIRCA,
        'fuzzy': fuzzy_methods.fMAIRCA
    },
    'MARCOS': {
        'crisp': crisp_methods.MARCOS
    },
    'MOORA': {
        'crisp': crisp_methods.MOORA,
        'fuzzy': fuzzy_methods.fMOORA
    },
    'OCRA': {
        'crisp': crisp_methods.OCRA,
        'fuzzy': fuzzy_methods.fOCRA
    },
    'PROBID': {
        'crisp': crisp_methods.PROBID,
    },
    'PROMETHEE': {
        'crisp': crisp_methods.PROMETHEE_II
    },
    'RIM': {
        'crisp': crisp_methods.RIM,
    },
    'SPOTIS': {
        'crisp': crisp_methods.SPOTIS
    },
    'TOPSIS': {
        'crisp': crisp_methods.TOPSIS,
        'fuzzy': fuzzy_methods.fTOPSIS
    },
    'VIKOR': {
        'crisp': crisp_methods.VIKOR,
        'fuzzy': fuzzy_methods.fVIKOR
    },
    "WASPAS": {
        'crisp': crisp_methods.WASPAS
    },
    'WPM': {
        'crisp': crisp_methods.WPM,
    },
    'WSM': {
        'crisp': crisp_methods.WSM,
    }
}