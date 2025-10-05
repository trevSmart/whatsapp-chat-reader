"""
WhatsApp Chat Reader

Una eina per processar xats exportats de WhatsApp i generar documents HTML
amb els adjunts integrats.
"""

__version__ = "1.0.0"
__author__ = "Marc Pla"
__email__ = "marc.pla@example.com"

from .parser import WhatsAppParser, WhatsAppMessage
from .html_generator import HTMLGenerator

__all__ = ["WhatsAppParser", "WhatsAppMessage", "HTMLGenerator"]
