#     data      topic                   state  retain  last-change  topic for change
d = { 
      'AC2AFB':['water-heater-leak/status','ON','true','true', 'last-leak'],
      'AC2AFA':['water-heater-leak/status','OFF','true','true', 'last-reset'],
      'AC2AFC':['water-heater-leak/battery','100','true','true', 'last-update'],

      'ABBAFB':['dishwasher-leak/status','ON','true','true', 'last-leak'],
      'ABBAFA':['dishwasher-leak/status','OFF','true','true', 'last-reset'],
      'ABBAFC':['dishwasher-leak/battery','100','true','true', 'last-update'],

      'ABEEFB':['ac-pan-leak/status','ON','true','true', 'last-leak'],
      'ABEEFA':['ac-pan-leak/status','OFF','true','true', 'last-reset'],
      'ABEEFC':['ac-pan-leak/battery','100','true','true', 'last-update']
    }

p = str(data.get('payload'))
t = str(data.get('time'))

if p is not None:
  if p in d.keys():
    service_data = {'topic':'home/nodes/sensor/{}'.format(d[p][0]), 'payload':'{}'.format(d[p][1]), 'qos':0, 'retain':'{}'.format(d[p][2])}
    if d[p][2] == 'true':
      last_change_data = {'topic':'home/nodes/sensor/{}/{}'.format(d[p][0], d[p][4]), 'payload':'{}'.format(t), 'qos':0, 'retain':'{}'.format(d[p][2])}
      hass.services.call('mqtt', 'publish', last_change_data, False)
  else:
    service_data = {'topic':'home/unknown', 'payload':'{}'.format(p), 'qos':0, 'retain':'false'}
    logger.warning('<rfbridge_demux> Received unknown RF command: {}'.format(p))
  hass.services.call('mqtt', 'publish', service_data, False)