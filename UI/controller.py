import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self.nerc = None

    def handleWorstCase(self, e):
        self._view._txtOut.clean
        max_years = int(self._view._txtYears.value)
        max_hours = int(self._view._txtHours.value)
        sequenza, persone, ore = self._model.worstCase(self.nerc, max_years, max_hours)
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {persone}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {ore}"))
        for po in sequenza:
            self._view._txtOut.controls.append(ft.Text(po))
        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n.id, text=n.value, data=n, on_click=self._readNerc))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

    def _readNerc(self, e):
        self.nerc = e.control.data
