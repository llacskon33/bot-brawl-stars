import os
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from brawl_api import BrawlStarsAPI, BrawlAPIError

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class BrawlStatsApp(App):
    def build(self):
        self.title = "Brawl Stars Stats"
        root = BoxLayout(orientation="vertical", padding=12, spacing=8)

        root.add_widget(Label(text="[b]Brawl Stars Stats[/b]", markup=True, font_size="22sp", size_hint_y=None, height=45))

        root.add_widget(Label(text="API key", size_hint_y=None, height=28, halign="left"))
        self.api_key_input = TextInput(
            text=os.getenv("BRAWL_API_KEY", ""),
            password=True,
            multiline=False,
            hint_text="Introduce tu API key",
            size_hint_y=None,
            height=44,
        )
        root.add_widget(self.api_key_input)

        root.add_widget(Label(text="Tag del jugador", size_hint_y=None, height=28, halign="left"))
        self.tag_input = TextInput(
            multiline=False,
            hint_text="#ABC123",
            size_hint_y=None,
            height=44,
        )
        root.add_widget(self.tag_input)

        self.search_button = Button(text="Consultar estadísticas", size_hint_y=None, height=48)
        self.search_button.bind(on_release=self.search_player)
        root.add_widget(self.search_button)

        scroll = ScrollView()
        self.result_label = Label(
            text="Introduce una API key y un tag de jugador.",
            markup=True,
            halign="left",
            valign="top",
            size_hint_y=None,
            padding=(8, 8),
        )
        self.result_label.bind(texture_size=self._resize_result)
        scroll.add_widget(self.result_label)
        root.add_widget(scroll)
        return root

    def _resize_result(self, label, size):
        label.height = max(size[1], 100)
        label.text_size = (label.width - 16, None)

    def search_player(self, *_):
        api_key = self.api_key_input.text.strip()
        tag = self.tag_input.text.strip()
        if not api_key:
            self.result_label.text = "[color=ff4444]Introduce una API key.[/color]"
            return
        if not tag:
            self.result_label.text = "[color=ff4444]Introduce el tag del jugador.[/color]"
            return

        self.search_button.disabled = True
        self.result_label.text = "Consultando..."
        Thread(target=self._request_player, args=(api_key, tag), daemon=True).start()

    def _request_player(self, api_key, tag):
        try:
            data = BrawlStarsAPI(api_key).get_player(tag)
            Clock.schedule_once(lambda *_: self._show_player(data), 0)
        except BrawlAPIError as exc:
            Clock.schedule_once(lambda *_: self._show_error(str(exc)), 0)
        except Exception as exc:
            Clock.schedule_once(lambda *_: self._show_error(f"Error inesperado: {exc}"), 0)

    def _show_player(self, data):
        club = data.get("club") or {}
        club_text = "Sin club"
        if club:
            club_text = f"{club.get('name', 'Sin nombre')} ({club.get('tag', 'sin tag')})"
        text = (
            f"[b]{data.get('name', 'Sin nombre')}[/b]\n"
            f"Tag: {data.get('tag', 'N/D')}\n\n"
            f"[b]Estadísticas[/b]\n"
            f"Trofeos: {data.get('trophies', 0)}\n"
            f"Récord de trofeos: {data.get('highestTrophies', 0)}\n"
            f"Nivel de experiencia: {data.get('expLevel', 0)}\n\n"
            f"[b]Victorias[/b]\n"
            f"3 contra 3: {data.get('3vs3Victories', 0)}\n"
            f"Solo: {data.get('soloVictories', 0)}\n"
            f"Dúo: {data.get('duoVictories', 0)}\n\n"
            f"[b]Club[/b]\n{club_text}\n\n"
            f"Brawlers: {len(data.get('brawlers', []))}"
        )
        self.result_label.text = text
        self.search_button.disabled = False

    def _show_error(self, message):
        self.result_label.text = f"[color=ff4444]{message}[/color]"
        self.search_button.disabled = False


if __name__ == "__main__":
    BrawlStatsApp().run()
