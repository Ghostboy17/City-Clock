

import os
import time
from datetime import datetime
import pytz
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.core.text import LabelBase
from kivy.uix.button import Button

import json

# Define la ruta para el archivo de configuración
CONFIG_FILE = "config.json"

# Register a custom font for LED style
LabelBase.register(name="Digital7", fn_regular="assets/fonts/digital-7.ttf")

# Define a dictionary with countries, their cities, and respective time zones
COUNTRY_CITIES_TIMEZONES = {
    "Ecuador": {
        "Quito": "America/Guayaquil",
        "Guayaquil": "America/Guayaquil",
        "Loja": "America/Guayaquil",
        "Cuenca": "America/Guayaquil",
        "Galapagos": "Pacific/Galapagos",
        "Tena": "America/Guayaquil",
    },
    "Colombia": {
        "Bogota": "America/Bogota",
        "Medellín": "America/Bogota",
        "Cali": "America/Bogota",
    },
    "Estados Unidos": {
        "Nueva York": "America/New_York",
        "Los Angeles": "America/Los_Angeles",
        "Chicago": "America/Chicago",
    },
    "Alemania": {
        "Berlin": "Europe/Berlin",
        "Hamburgo": "Europe/Berlin",
        "Munich": "Europe/Berlin",
    },
    "Japón": {
        "Tokio": "Asia/Tokyo",
        "Osaka": "Asia/Tokyo",
        "Kioto": "Asia/Tokyo",
    },

    "South Korea": {
        "Seoul": "Asia/Seoul",
    },
    "North Korea": {
        "Pyongyang": "Asia/Pyongyang",
    },

    "España": {
        "Madrid": "Europe/Madrid",
    },
    "Peru": {
        "Lima": "America/Lima",
    },
    "Venezuela": {
        "Caracas": "America/Caracas",
    },
    "Argentina": {
        "Buenos Aires": "America/Buenos_Aires",
    },
    "Chile": {
        "Santiago de Chile": "America/Santiago",
    },
    "Brazil": {
        "Brasilia": "Brazil/East",
    },
}

# Define a dictionary with backgrounds for each city
CITY_BACKGROUNDS = {
    "Quito": ["assets/ST-America/Ecuador/Quito/quito1.jpg", "assets/ST-America/Ecuador/Quito/quito2.jpg", "assets/ST-America/Ecuador/Quito/quito3.jpg", "assets/ST-America/Ecuador/Quito/quito4.jpg",],
    "Guayaquil": ["assets/ST-America/Ecuador/Guayaquil/guayaquil1.jpg", "assets/ST-America/Ecuador/Guayaquil/guayaquil2.jpg", "assets/ST-America/Ecuador/Guayaquil/guayaquil3.jpg",],
    "Loja": ["assets/ST-America/Ecuador/Loja/loja1.jpg", "assets/ST-America/Ecuador/Loja/loja2.jpg", "assets/ST-America/Ecuador/Loja/loja3.jpg", "assets/ST-America/Ecuador/Loja/loja4.jpg"],
    "Galapagos": ["assets/ST-America/Ecuador/Galapagos/galapagos1.jpg", "assets/ST-America/Ecuador/Galapagos/galapagos2.jpg", "assets/ST-America/Ecuador/Galapagos/galapagos3.jpg", "assets/ST-America/Ecuador/Galapagos/galapagos4.jpg", "assets/ST-America/Ecuador/Galapagos/galapagos5.jpg",],
    "Cuenca": ["assets/ST-America/Ecuador/Cuenca/cuenca1.jpg", "assets/ST-America/Ecuador/Cuenca/cuenca2.jpg", "assets/ST-America/Ecuador/Cuenca/cuenca3.jpg", "assets/ST-America/Ecuador/Cuenca/cuenca4.jpg", "assets/ST-America/Ecuador/Cuenca/cuenca5.jpg",],
    "Tena": ["assets/ST-America/Ecuador/Tena/tena1.jpg", "assets/ST-America/Ecuador/Tena/tena2.jpg", "assets/ST-America/Ecuador/Tena/tena3.jpg", "assets/ST-America/Ecuador/Tena/tena4.jpg", "assets/ST-America/Ecuador/Tena/tena5.jpg",],
    
    "Bogota": ["assets/ST-America/Colombia/Bogota/bogota1.jpg", "assets/ST-America/Colombia/Bogota/bogota2.jpg",],
    "Medellin": ["assets/ST-America/Colombia/Medellin/medellin1.jpg", "assets/ST-America/Colombia/Medellin/medellin2.jpg", "assets/ST-America/Colombia/Medellin/medellin3.jpg",],
    "Cali": ["assets/ST-America/Colombia/Cali/cali1.jpg", "assets/ST-America/Colombia/Cali/cali2.jpg", "assets/ST-America/Colombia/Cali/cali3.jpg",],

    "Caracas": ["assets/ST-America/Venezuela/Caracas/caracas1.jpg", "assets/ST-America/Venezuela/Caracas/caracas2.jpg", "assets/ST-America/Venezuela/Caracas/caracas3.jpg",],

    "Lima": ["assets/ST-America/Peru/Lima/lima1.jpg", "assets/ST-America/Peru/Lima/lima2.jpg", "assets/ST-America/Peru/Lima/lima3.jpg",],

    "Brasilia": ["assets/ST-America/Brazil/Brasilia/brasilia1.jpg", "assets/ST-America/Brazil/Brasilia/brasilia2.jpg", "assets/ST-America/Brazil/Brasilia/brasilia3.jpg",],

    "Buenos Aires": ["assets/ST-America/Argentina/Buenos_Aires/buenos_aires1.jpg", "assets/ST-America/Argentina/Buenos_Aires/buenos_aires2.jpg", "assets/ST-America/Argentina/Buenos_Aires/buenos_aires3.jpg",],

    "Santiago de Chile": ["assets/ST-America/Chile/Sto_Chile/sto_chile1.jpg", "assets/ST-America/Chile/Sto_Chile/sto_chile2.jpg", "assets/ST-America/Chile/Sto_Chile/sto_chile3.jpg",],

    "Nueva York": ["assets/NT-America/U.S.A/New_York/new_york1.jpg", "assets/NT-America/U.S.A/New_York/new_york2.jpg", "assets/NT-America/U.S.A/New_York/new_york3.jpg", "assets/NT-America/U.S.A/New_York/new_york4.jpg",],
    "Los Angeles": ["assets/NT-America/U.S.A/Los_Angeles/los_angeles1.jpg", "assets/NT-America/U.S.A/Los_Angeles/los_angeles2.jpg", "assets/NT-America/U.S.A/Los_Angeles/los_angeles3.jpg", "assets/NT-America/U.S.A/Los_Angeles/los_angeles4.jpg",],
    "Chicago": ["assets/NT-America/U.S.A/Chicago/chicago1.jpg", "assets/NT-America/U.S.A/Chicago/chicago2.jpg", "assets/NT-America/U.S.A/Chicago/chicago3.jpg"],

    "Berlín": ["assets/backgrounds/berlin1.jpg", "assets/backgrounds/berlin2.jpg"],
   
    "Tokio": ["assets/backgrounds/tokyo1.jpg", "assets/backgrounds/tokyo2.jpg"],

    "Tokio": ["assets/Asia/Japan/tokio1.jpg", "assets/Asia/Japan/tokio2.jpg", "assets/Asia/Japan/tokio3.jpg",],
    
    "Seoul": ["assets/Asia/Korea_S/Seoul/seoul1.jpg", "assets/Asia/Korea_S/Seoul/seoul2.jpg","assets/Asia/Korea_S/Seoul/seoul3.jpg",],

    "Pyongyang": ["assets/Asia/Korea_N/Pyongyang/pyongyang1.jpg", "assets/Asia/Korea_N/Pyongyang/pyongyang2.jpg", "assets/Asia/Korea_N/Pyongyang/pyongyang3.jpg",],

    "Madrid": ["assets/Europe/Espana/Madrid/madrid1.jpg", "assets/Europe/Espana/Madrid/madrid2.jpg", "assets/Europe/Espana/Madrid/madrid3.jpg",],

    "Berlin": ["assets/Europe/Alemania/Berlin/berlin1.jpg", "assets/Europe/Alemania/Berlin/berlin2.jpg", "assets/Europe/Alemania/Berlin/berlin3.jpg",],
    "Hamburgo": ["assets/Europe/Alemania/Hamburgo/hamburgo1.jpg", "assets/Europe/Alemania/Hamburgo/hamburgo2.jpg", "assets/Europe/Alemania/Hamburgo/hamburgo3.jpg",],
    "Munich": ["assets/Europe/Alemania/Munich/munich1.jpg", "assets/Europe/Alemania/Munich/munich2.jpg", "assets/Europe/Alemania/Munich/munich3.jpg",],




}

#python main.py

class WorldClockApp(App):
    def build(self):
        # Cargar la configuración inicial desde el archivo
        self.config = self.load_config()

        # Configuración predeterminada
        self.current_country = self.config.get("country", "Ecuador")
        self.current_city = self.config.get("city", "Quito")
        self.current_color = self.config.get("color", (1, 0, 0, 1))  # Rojo por defecto

        # Set the window size (for desktop testing)
        Window.size = (800, 600)

        # Main layout
        self.layout = BoxLayout(orientation='vertical')

        # Background initialization
        self.background_index = 0
        self.update_background()

        # Label for the clock
        self.clock_label = Label(
            text="",
            font_size=72,
            bold=True,
            color=self.current_color,  # Color desde la configuración
            font_name="Digital7",  # Usa la fuente registrada
            size_hint=(1, 0.7)
        )

        # Spinner for selecting a country
        self.country_spinner = Spinner(
            text=self.current_country,
            values=list(COUNTRY_CITIES_TIMEZONES.keys()),
            size_hint=(0.13, 0.1)
        )
        self.country_spinner.bind(text=self.on_country_selected)

        # Spinner for selecting a city
        self.city_spinner = Spinner(
            text=self.current_city,
            values=list(COUNTRY_CITIES_TIMEZONES[self.current_country].keys()),
            size_hint=(0.13, 0.1)
        )
        self.city_spinner.bind(text=self.on_city_selected)

        # Botón para cambiar el color
        self.color_button = Button(
            text="Cambiar Color",
            size_hint=(0.13, 0.1)
        )
        self.color_button.bind(on_press=self.change_clock_color)

        # Add widgets to layout
        self.layout.add_widget(self.clock_label)
        self.layout.add_widget(self.country_spinner)
        self.layout.add_widget(self.city_spinner)
        self.layout.add_widget(self.color_button)

        # Schedule clock updates
        Clock.schedule_interval(self.update_clock, 1)

        # Schedule background updates
        Clock.schedule_interval(self.rotate_background, 20)

        return self.layout

    def load_config(self):
        """Cargar la configuración desde un archivo JSON."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_config(self):
        """Guardar la configuración actual en un archivo JSON."""
        with open(CONFIG_FILE, "w") as file:
            json.dump(
                {
                    "country": self.current_country,
                    "city": self.current_city,
                    "color": self.current_color,
                },
                file,
            )

    def update_clock(self, dt):
        """Update the clock label with the current time in the selected city."""
        tz = pytz.timezone(COUNTRY_CITIES_TIMEZONES[self.current_country][self.current_city])
        current_time = datetime.now(tz).strftime('%H:%M:%S')
        self.clock_label.text = f"{self.current_city}: {current_time}"

    def on_country_selected(self, spinner, text):
        """Handle country selection from the spinner."""
        self.current_country = text
        # Update city spinner options based on selected country
        self.city_spinner.values = list(COUNTRY_CITIES_TIMEZONES[self.current_country].keys())
        self.city_spinner.text = list(COUNTRY_CITIES_TIMEZONES[self.current_country].keys())[0]  # Default to first city
        self.on_city_selected(self.city_spinner, self.city_spinner.text)

    def on_city_selected(self, spinner, text):
        """Handle city selection from the spinner."""
        self.current_city = text
        self.update_background()
        self.save_config()  # Guardar la configuración actualizada

    def update_background(self):
        """Update the background image based on the selected city."""
        backgrounds = CITY_BACKGROUNDS.get(self.current_city, ["assets/backgrounds/default.jpg"])
        self.background_index = 0  # Reset index for new city

        # Set the first image as background
        with self.layout.canvas.before:
            self.layout.canvas.before.clear()
            Color(1, 1, 1, 1)  # Reset color to white
            self.bg_rect = Rectangle(
                source=backgrounds[self.background_index],
                pos=self.layout.pos,
                size=Window.size
            )

    def rotate_background(self, dt):
        """Rotate the background images every 10 seconds."""
        backgrounds = CITY_BACKGROUNDS.get(self.current_city, ["assets/backgrounds/default.jpg"])
        self.background_index = (self.background_index + 1) % len(backgrounds)

        # Update the background image
        with self.layout.canvas.before:
            self.layout.canvas.before.clear()
            Color(1, 1, 1, 1)  # Reset color to white
            self.bg_rect = Rectangle(
                source=backgrounds[self.background_index],
                pos=self.layout.pos,
                size=Window.size
            )

    def change_clock_color(self, instance):
        """Cambiar el color de los números del reloj."""
    # Lista de colores predefinidos
        color_options = [
            (1, 0, 0, 1),  # Rojo
            (0, 1, 0, 1),  # Verde
            (0, 0, 1, 1),  # Azul
            (1, 0.5, 0, 1),  # Naranja

            (1, 1, 0, 1),  # Amarillo
            (1, 1, 1, 1),  # Blanco
        ]

        # Convertir el color actual en tupla para evitar problemas de comparación
        current_color_tuple = tuple(self.current_color)

        # Cambiar al siguiente color en la lista
        if current_color_tuple in color_options:
            current_index = color_options.index(current_color_tuple)
            self.current_color = color_options[(current_index + 1) % len(color_options)]
        else:
            # Si el color actual no está en la lista, establecer el primero como predeterminado
            self.current_color = color_options[0]

        # Actualizar el color del texto del reloj
        self.clock_label.color = self.current_color

        # Guardar el nuevo color en la configuración
        self.save_config()

        

if __name__ == "__main__":
    WorldClockApp().run()