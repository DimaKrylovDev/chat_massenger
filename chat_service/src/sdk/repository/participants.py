from .base import BaseRepository
from models.participants import Participants
from schemas.participant import Participant as ParticipantSchema

class ParticipantsRepository(BaseRepository):
    model = Participants
    model_schema = ParticipantSchema