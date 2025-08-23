class TestURLShortener:
    def test_redirect_invalid_length(self, client):
        response = client.get("/abcdef")
        assert response.status_code == 400
        detail = response.json()["detail"]
        assert detail == "Short URL must be exactly 5 characters."

    def test_shorten_and_redirect(self, client):
        response = client.post("/shorten", json={"url": "https://example.com"})
        assert response.status_code == 200
        short_url = response.json()["short_url"]
        assert len(short_url) == 5

        response = client.get(f"/{short_url}", follow_redirects=False)
        assert response.status_code == 307
        location = response.headers["location"]
        assert location.rstrip("/") == "https://example.com"

    def test_invalid_url(self, client):
        response = client.post("/shorten", json={"url": "not-a-url"})
        assert response.status_code == 422

    def test_reuse_existing_url(self, client):
        # First call
        resp1 = client.post("/shorten/", json={"url": "https://google.com"})
        # Second call for same URL
        resp2 = client.post("/shorten/", json={"url": "https://google.com"})

        assert resp1.json()["short_url"] == resp2.json()["short_url"]

    def test_redirect_not_found(self, client):
        response = client.get("/abcde", follow_redirects=False)
        assert response.status_code == 404
        assert response.json()["detail"] == "Short URL not found."
