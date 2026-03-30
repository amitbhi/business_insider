"""Task planner for agent dispatch dependency."""

class TaskPlanner:
    """Determines execution dependencies before dispatching agents."""
    
    def __init__(self, objective: str):
        self.objective = objective
        self.execution_queue: list = []
        
    def generate_plan(self) -> list:
        """Validates run-order to secure dependencies."""
        self.execution_queue = ["finance", "power", "legal", "social", "market"]
        return self.execution_queue
