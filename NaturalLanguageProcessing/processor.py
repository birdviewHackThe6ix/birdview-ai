

class Processor:
    def __init__(self, ):
        self.content = ''

    def form_address_from_components(self, entities):
        people = []
        companies = []
        addresses = []
        print(entities)
        for entity in entities:
            if entity['type'] == 'PERSON':  people.append(entity['name'])
            elif entity['type'] == 'ORGANIZATION':  companies.append(entity['name'])
            elif entity['type'] == 'LOCATION':  addresses.append(entity['name'])
        return '{}, {}'.format(', '.join(companies), ', '.join(addresses))
