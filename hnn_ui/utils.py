import io


# Set cfg params from .param file
def set_cfg_from_file (fn, cfg):
    return set_cfg_from_params(open(fn, "rb").read(), cfg)


# Set cfg params from .param string
def set_cfg_from_params(fn, cfg):
    d = {}
    with io.BytesIO(fn) as fp:
        ln = fp.readlines()
        for l in ln:
            s = l.decode('utf-8').strip()
            if s.startswith('#'): continue
            sp = s.split(':')
            sp[1] = sp[1].strip()
            if len(sp[1]) > 0:
                if '.' in sp[1] or 'e' in sp[1]:
                    try:
                        value = float(sp[1])
                    except:
                        value = str(sp[1])
                else:
                    try:
                        value = int(sp[1])
                    except:
                        value = str(sp[1])

                d[sp[0].strip()] = value

    for k, v in d.items():
        setattr(cfg, k, v)

    cfg.duration = cfg.tstop
    return cfg
