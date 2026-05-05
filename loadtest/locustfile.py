from locust import HttpUser, task, between

class PortfolioUser(HttpUser):
    # Wait 1-3 seconds between requests
    # Simulates real user behavior
    wait_time = between(1, 3)

    # @task means Locust will call this function
    # The number in @task() is the weight
    # @task(3) = called 3x more often than @task(1)

    @task(3)
    def visit_homepage(self):
        """Simulate user visiting the main page"""
        self.client.get("/")

    @task(2)
    def check_health(self):
        """Simulate monitoring system checking health"""
        self.client.get("/health")

    @task(1)
    def check_info(self):
        """Simulate user checking app info"""
        self.client.get("/info")

    @task(1)
    def check_metrics(self):
        """Simulate Prometheus scraping metrics"""
        self.client.get("/metrics")