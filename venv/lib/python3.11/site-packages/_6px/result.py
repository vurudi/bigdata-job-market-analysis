class Result:
    def __init__(self, data):
        self.data = data['processed']
        self.outputs = {}

        for item in self.data:
            self.outputs[item['name']] = ResultOutput(item)

    def get_output(self, outputName):
    	return self.outputs[outputName]


class ResultOutput:
    def __init__(self, data):
        self.data = data
        self.refs = {}

        for (index, item) in self.data['data']['output'].iteritems():
            self.refs[index] = item

    def get_location(self, refName):
        return self.refs[refName]['location']

    def get_width(self, refName):
        return self.refs[refName]['info']['width']

    def get_height(self, refName):
        return self.refs[refName]['info']['height']

    def get_size(self, refName):
        return self.refs[refName]['info']

    def get_bytes(self, refName):
        return self.refs[refName]['info']['bytes']

class ResultInfo:
    def __init__(self, data):
        self.data = data.get_output('info')

    def get_width(self, refName):
        return self.data.get_width(refName)

    def get_height(self, refName):
        return self.data.get_height(refName)

    def get_bytes(self, refName):
        return self.data.get_bytes(refName)

    def get_size(self, refName):
        return self.data.get_size(refName)
