class TestHealthCheckView:

    def test_health_check(self, flask_test_client):
        res = flask_test_client.get('/api/health_check')
        assert res.status_code == 200
        assert res.data.decode("utf-8").rstrip('\n') == 'true'
