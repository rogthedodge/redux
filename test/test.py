from source import redux_DB

x = redux_DB.redux_model()
y = x.get_next_person_to_call('Cus March')
print(y)
