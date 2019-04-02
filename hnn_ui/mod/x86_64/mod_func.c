#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _ar_reg(void);
extern void _beforestep_py_reg(void);
extern void _cad_reg(void);
extern void _ca_reg(void);
extern void _cat_reg(void);
extern void _dipole_reg(void);
extern void _dipole_pp_reg(void);
extern void _hh2_reg(void);
extern void _kca_reg(void);
extern void _km_reg(void);
extern void _lfp_reg(void);
extern void _mea_reg(void);
extern void _vecevent_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," ar.mod");
    fprintf(stderr," beforestep_py.mod");
    fprintf(stderr," cad.mod");
    fprintf(stderr," ca.mod");
    fprintf(stderr," cat.mod");
    fprintf(stderr," dipole.mod");
    fprintf(stderr," dipole_pp.mod");
    fprintf(stderr," hh2.mod");
    fprintf(stderr," kca.mod");
    fprintf(stderr," km.mod");
    fprintf(stderr," lfp.mod");
    fprintf(stderr," mea.mod");
    fprintf(stderr," vecevent.mod");
    fprintf(stderr, "\n");
  }
  _ar_reg();
  _beforestep_py_reg();
  _cad_reg();
  _ca_reg();
  _cat_reg();
  _dipole_reg();
  _dipole_pp_reg();
  _hh2_reg();
  _kca_reg();
  _km_reg();
  _lfp_reg();
  _mea_reg();
  _vecevent_reg();
}
