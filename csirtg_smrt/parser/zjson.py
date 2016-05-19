import copy
import json
from csirtg_smrt.parser import Parser
from csirtg_indicator.utils import normalize_itype
from csirtg_indicator import Indicator


class Json(Parser):

    def __init__(self, *args, **kwargs):
        super(Json, self).__init__(*args, **kwargs)

    def process(self):
        defaults = self._defaults()
        map = self.rule.feeds[self.feed]['map']
        values = self.rule.feeds[self.feed]['values']

        data = []
        for l in self.fetcher.process():
            i = copy.deepcopy(defaults)

            l = json.loads(l)
            for e in l:
                i = {}
                for x, c in enumerate(map):
                    i[values[x]] = e[c]

                try:
                    self.logger.debug(i)
                    i = normalize_itype(i)
                    i = Indicator(**i)
                    r = self.client.indicators_create(i)
                    data.append(r)
                except NotImplementedError as e:
                    self.logger.error(e)
                    self.logger.info('skipping: {}'.format(i['indicator']))

        return data

Plugin = Json