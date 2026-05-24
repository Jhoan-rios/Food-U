from datetime import datetime, time, timedelta


DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes"]


EDIFICIOS = {
    "bloque 1": "restaurante coliseo",
    "bloque 2": "restaurante coliseo",
    "bloque 3": "restaurante ingenieria",
    "bloque 4": "restaurante ingenieria",
    "bloque 5": "restaurante ingenieria",
    "bloque 6": "restaurante ingenieria",
    "bloque 7": "restaurante ingenieria",
    "bloque 10": "kiosko comunicaciones",
    "bloque 11": "kiosko comunicaciones",
    "bloque 12": "kiosko comunicaciones",
    "bloque 14": "restaurante derecho",
    "bloque 15": "restaurante derecho",
    "bloque 16": "restaurante derecho",
    "bloque 17": "cafeteria teatro",
    "bloque 18": "cafeteria teatro",
    "biblioteca": "cafetería central",
    "default": "cafetería central",
}

class Clase:

    def __init__(self, nombre: str, dia: str, hora_inicio: str, hora_fin: str, salon: str = ""):
        self.nombre = nombre
        self.dia = dia.lower()
        self.hora_inicio = self._parse_hora(hora_inicio)
        self.hora_fin = self._parse_hora(hora_fin)
        self.salon = salon.lower() if salon else ""

    def _parse_hora(self, hora_str: str) -> time:
        return datetime.strptime(hora_str, "%H:%M").time()

    def duracion_minutos(self) -> int:
        inicio = datetime.combine(datetime.today(), self.hora_inicio)
        fin = datetime.combine(datetime.today(), self.hora_fin)
        return int((fin - inicio).total_seconds() / 60)

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "dia": self.dia,
            "hora_inicio": self.hora_inicio.strftime("%H:%M"),
            "hora_fin": self.hora_fin.strftime("%H:%M"),
            "salon": self.salon,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Clase":
        return cls(
            nombre=data["nombre"],
            dia=data["dia"],
            hora_inicio=data["hora_inicio"],
            hora_fin=data["hora_fin"],
            salon=data.get("salon", ""),
        )

class EspacioLibre:

    def __init__(self, dia: str, inicio: time, fin: time, clase_siguiente: "Clase | None" = None):
        self.dia = dia
        self.inicio = inicio
        self.fin = fin
        self.clase_siguiente = clase_siguiente
        self.duracion = self._calcular_duracion()

    def _calcular_duracion(self) -> int:
        i = datetime.combine(datetime.today(), self.inicio)
        f = datetime.combine(datetime.today(), self.fin)
        return int((f - i).total_seconds() / 60)

    @property
    def alcanza_para_comer(self) -> bool:
        return self.duracion >= 15

    @property
    def alcanza_para_recoger(self) -> bool:
        return self.duracion >= 5

    @property
    def hora_preorden(self) -> time:
        dt = datetime.combine(datetime.today(), self.inicio) - timedelta(minutes=20)
        return dt.time()

    @property
    def punto_venta_sugerido(self) -> str:
        if self.clase_siguiente and self.clase_siguiente.salon:
            salon = self.clase_siguiente.salon
            for key, cafeteria in EDIFICIOS.items():
                if key in salon:
                    return cafeteria
        return EDIFICIOS["default"]

    @property
    def modo(self) -> str:
        if self.duracion >= 30:
            return "comer_tranquilo"
        elif self.duracion >= 15:
            return "comer_rapido"
        elif self.duracion >= 5:
            return "solo_recoger"
        else:
            return "sin_tiempo"

    def descripcion_modo(self) -> str:
        descripciones = {
            "comer_tranquilo": "🍽️ Tienes tiempo suficiente para comer tranquilo.",
            "comer_rapido":    "⚡ Tiempo justo — mejor pre-ordena para que esté listo.",
            "solo_recoger":    "🏃 Solo alcanzas a recoger. Pre-ordena ya.",
            "sin_tiempo":      "❌ No hay tiempo suficiente para pedir.",
        }
        return descripciones[self.modo]


