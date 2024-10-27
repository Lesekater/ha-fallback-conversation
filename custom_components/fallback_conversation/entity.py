import asyncio

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.components.conversation.models import ConversationResult
from homeassistant.config_entries import ConfigEntry

class FallbackResultEntity(SensorEntity):
    """Entity to store the latest fallback result."""

    entry: ConfigEntry
    hass: HomeAssistant

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize the entity."""
        self.hass = hass
        self.entry = entry
        self._attr_name = f"{entry.title} Result"
        self._attr_unique_id = f"{entry.entry_id}_result"
        self._state = None
        self._attributes = {}
        self.entity_id = ENTITY_ID_FORMAT.format(self._attr_unique_id)

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

    async def update_result(self, agent_name, prompt: str, result: ConversationResult):
        """Update the entity with the latest fallback result."""

        plain_text_response = ""
        if result.response.speech.plain:
            plain_text_response = result.response.speech.plain.speech

        formatted_state: str = f"""
        [Agent]:{agent_name},
        [Prompt]:{prompt},
        [Response]:{plain_text_response}
        """

        self._state = formatted_state
        self._attributes = result.response.as_dict()
        self.async_write_ha_state()
