from types import SimpleNamespace

# Define states for state monitors
state = SimpleNamespace(**{
    'VOLTAGE': 'v',
    'CURRENT': 'I',
    'X1TRACE': 'x1',
    'X2TRACE': 'x2',
    'Y1TRACE': 'y1',
    'Y2TRACE': 'y2',
    'Y3TRACE': 'y3',
    'WEIGHT': 'w',
    'ACTUAL_WEIGHT': 'w_act'
})

# Synapse sign mode
synapse_sign_mode = SimpleNamespace(**{
    'MIXED': 1,
    'EXCITATORY': 2,
    'INHIBITORY': 3
})
