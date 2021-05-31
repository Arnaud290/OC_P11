from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        self.client.post(
            "/showSummary",
            {"email": "john@simplylift.co"}
        )

    @task
    def index(self):
        self.client.get("/")

    @task
    def purchasePlaces(self):
        self.client.post(
            '/purchasePlaces',
            data={
                'club': 'Simply Lift',
                'competition': 'Spring Festival',
                'places': '3'
            }
        )
