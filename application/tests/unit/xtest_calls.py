
def test_home_page(test_client):
    response = test_client.get('/')
    assert 200 == response.status_code

    response = test_client.post('/')
    assert 404 == response.status_code


def test_documentation_page(test_client):
    response = test_client.get('/v1/documentation')
    assert 200 == response.status_code

    response = test_client.post('/v1/documentation')
    assert 404 == response.status_code

# Ten zmetek bohuzel z me zahadneho duvodu nenacte /app.py , takze se routy neprojevuji - a pada to; proto vypnute
