from src.models import Ticket

def test_ticket_key():
    t = Ticket((1, 2, 3, 4, 5), (1, 2))
    assert t.key() == ((1, 2, 3, 4, 5), (1, 2))
