import copy

from database.DAO import DAO


class Model:
    def __init__(self):

        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.max_persone = 0



    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self.max_persone = 0
        poweroutages = DAO.getAllEvents(nerc)
        self.ricorsione([], maxY, maxH, poweroutages)
        return self._solBest, self.max_persone, self.calcola_durata(self._solBest)/3600


    def ricorsione(self, parziale, maxY, maxH, pos):
        if len(pos) == 0:
            p = self.calcola_persone(parziale)
            if p > self.max_persone:
                print(p)
                self._solBest = copy.deepcopy(parziale)
                self.max_persone = p
        else:
            for po in pos:
                parziale.append(po)
                nuovi_rimanenti = self.calcola_rimanenti(maxY, maxH, parziale, pos)
                self.ricorsione(parziale, maxY, maxH, nuovi_rimanenti)
                parziale.pop()

    def calcola_rimanenti(self, maxY, maxH, parziale, pos):
        nuovi_rimanenti = []
        for e in pos:
            if self.is_ok(parziale, e, maxY, maxH):
                nuovi_rimanenti.append(e)
        return nuovi_rimanenti

    def is_ok(self, parziale, po, maxY, maxH):

        tot_ore = self.calcola_durata(parziale)
        if tot_ore + self.durata(po) > maxH*3600:
            return False

        if abs(po.date_event_began.year - po.date_event_began.year) > maxY:
            return False

        for e in parziale:
            if e == po:
                return False

        return True

    def calcola_persone(self, parziale):
        tot = 0
        for po in parziale:
            tot += po.customers_affected
        return tot

    def calcola_durata(self, parziale):
        if len(parziale) == 0:
            return 0
        sum = 0
        for event in parziale:
            sum += self.durata(event)
        return sum

    def durata(self, event):
        return (event.date_event_finished - event.date_event_began).total_seconds()

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc

