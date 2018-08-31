from dash.dependencies import Input, Output, State


def _camelify(name, delims=None):
    
    delims = delims or ['-', '_']
    chars = []
    headsup = False
    
    for c in name:
        if headsup:
            chars.append(c.upper())
            headsup = False
        elif c in delims:
            headsup = True
        else:
            chars.append(c)
            
    return ''.join(chars)

            
def _decamelify(name, delim='-'):
    
    chars = [name[0].lower()]
    
    for c in name[1:]:
        if c == c.upper():
            chars.append(delim)
            chars.append(c.lower())
        else:
            chars.append(c)
            
    return ''.join(chars)


class Data:
    
    def __init__(self, data=None):
        self.data = data or {}
        
        
    def __getitem__(self, key):
        return self.data[key]
        
        
    def __getattr__(self, key):
        if key == 'data':
            return self.data
        else:
            return self.data[key]

        
class Component:
    
    def __init__(self, id):
        self.id = id
        
        
    def output(self, key):
        return Output(self.id, key)
    
    
    def input(self, key):
        return Input(self.id, key)
    
    
    def state(self, key):
        return State(self.id, key)
        
        
    def __getitem__(self, key):
        return (self.id, key)
    
    
class Block:

    def __init__(self, app=None, data=None, id='', **kwargs):
        
        self.app = app
        self.data = Data(data)
        self.base_id = self.block_id()
        self.ids = {'this': self.base_id + id}
        
        self.parameters(**kwargs)
        self.layout = self.layout()
        
        
    def parameters(self, **kwargs):
        pass
        
        
    def block_id(self):
        return _decamelify(self.__class__.__name__)

    
    def layout(self):
        raise NotImplementedError
        
        
    def callbacks(self):
        pass

    
    def register(self, id, full_id=None):
        if full_id is None:
            full_id = '{}-{}'.format(self.ids['this'], id)
        self.ids.update({id: full_id})
        return full_id
    
    
    def __getitem__(self, key):
        return Component(self.ids[key])
    
    
    def __call__(self, component_id, property_id=None):
        
        if component_id not in self.ids:
            self.register(component_id)
            
        if property_id is None:
            return self.ids[component_id]
        else:
            return self[component_id][property_id]
    
    
    def output(self, component_id, component_property):
        return self[component_id].output(component_property)
    
    
    def input(self, component_id, component_property):
        return self[component_id].input(component_property)
    
    
    def state(self, component_id, component_property):
        return self[component_id].state(component_property)
    
    
