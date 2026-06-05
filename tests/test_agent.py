import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.tools import agent_tools
from langchain_core.tools import BaseTool

class TestAgentTools(unittest.TestCase):
    def test_tools_exist(self):
        self.assertTrue(len(agent_tools) > 0)
        
    def test_tool_types(self):
        for tool in agent_tools:
            self.assertTrue(isinstance(tool, BaseTool))
            self.assertIsNotNone(tool.name)
            self.assertIsNotNone(tool.description)

if __name__ == '__main__':
    unittest.main()
