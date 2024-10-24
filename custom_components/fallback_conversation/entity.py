import asyncio

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.components.conversation.models import ConversationResult

class FallbackResultEntity(SensorEntity, RestoreEntity):
    """Entity to store the latest fallback result."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the entity."""
        self.hass = hass
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the entity."""
        return "Fallback Conversation Result"

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            self._attributes = dict(state.attributes)

    def update_result(self, agent_name, result: ConversationResult):
        """Update the entity with the latest fallback result."""
        self._state = agent_name
        self._attributes = {
            "response": result.response,
        }
        self.async_write_ha_state()

    async def async_get_last_state(self):
        """Get the last state of the entity."""
        states = await self.hass.states.async_get(ENTITY_ID_FORMAT.format("sensor.fallback_conversation_result"))
        return states