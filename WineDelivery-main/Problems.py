import copy
import random


class ItalyProblems(object):
            
            graph = {'Torino' : [{'Genoa':75},{'Milano':118},{'Firenze':140}],
                     'Genoa' : [{'Bologna':71},{'Torino':75}],
                     'Bologna' : [{'Genoa':71},{'Firenze':151}],
                     'Milano' : [{'Torino':118},{'Venezia':111}],
                     'Venezia' : [{'Milano':111},{'Trieste':70}],
                     'Trieste' : [{'Venezia':70},{'Trento':75}],
                     'Trento' : [{'Trieste':75},{'Ancona':120}],
                     'Ancona' : [{'Trento':120},{'Perugia':146},{'Aquila':138}],
                     'Firenze' : [{'Bologna':151},{'Torino':140},{'Perugia':80},{'Siena':99}],
                     'Perugia' : [{'Firenze':80},{'Ancona':146},{'Aquila':97}],
                     'Aquila' : [{'Perugia':97},{'Ancona':138},{'Roma':101}],
                     'Siena' : [{'Firenze':99},{'Roma':211}],
                     'Cagliari' : [{'Roma':90}],
                     'Roma' : [{'Aquila':101},{'Cagliari':90},{'Napoli':85}],
                     'Napoli' : [{'Roma':85},{'Potenza':98},{'Foggia':142}],
                     'Potenza' : [{'Napoli':98},{'Palermo':86}],
                     'Palermo' : [{'Potenza':86}],
                     'Foggia' : [{'Napoli':142},{'Bari':92}],
                     'Bari' : [{'Foggia':92},{'Lecce':87}],
                     'Lecce' : [{'Bari':87}]
                    }
            
            defalut_h_values = {
                'Torino':366,
                'Milano':329,
                'Firenze':253,
                'Genoa':374,
                'Venezia':244,
                'Perugia':193,
                'Siena':178,
                'Bologna':380,
                'Trieste':241,
                'Ancona':160,
                'Aquila':98,
                'Roma':0,
                'Trento':242,
                'Cagliari':77,
                'Napoli':80,
                'Potenza':151,
                'Palermo':161,
                'Foggia':199,
                'Bari':226,
                'Lecce':234
            }

