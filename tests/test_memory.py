import unittest
import tempfile
import os
from core.memory.conversation_store import ConversationStore

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.store = ConversationStore(self.temp_db.name)

    def tearDown(self):
        os.unlink(self.temp_db.name)

    def test_save(self):
        self.store.save("hello", "hi", "normal")
        # Test passes if no exception

if __name__ == '__main__':
    unittest.main()
