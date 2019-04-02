/* Created by Language version: 7.5.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__mea
#define _nrn_initial _nrn_initial__mea
#define nrn_cur _nrn_cur__mea
#define _nrn_current _nrn_current__mea
#define nrn_jacob _nrn_jacob__mea
#define nrn_state _nrn_state__mea
#define _net_receive _net_receive__mea 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define initial_part_line0 _p[0]
#define initial_part_line1 _p[1]
#define initial_part_line2 _p[2]
#define initial_part_line3 _p[3]
#define initial_part_line4 _p[4]
#define initial_part_line5 _p[5]
#define initial_part_line6 _p[6]
#define initial_part_line7 _p[7]
#define initial_part_line8 _p[8]
#define initial_part_line9 _p[9]
#define initial_part_line10 _p[10]
#define initial_part_line11 _p[11]
#define initial_part_line12 _p[12]
#define initial_part_line13 _p[13]
#define initial_part_line14 _p[14]
#define initial_part_line15 _p[15]
#define mea_line0 _p[16]
#define mea_line1 _p[17]
#define mea_line2 _p[18]
#define mea_line3 _p[19]
#define mea_line4 _p[20]
#define mea_line5 _p[21]
#define mea_line6 _p[22]
#define mea_line7 _p[23]
#define mea_line8 _p[24]
#define mea_line9 _p[25]
#define mea_line10 _p[26]
#define mea_line11 _p[27]
#define mea_line12 _p[28]
#define mea_line13 _p[29]
#define mea_line14 _p[30]
#define mea_line15 _p[31]
#define _g _p[32]
#define transmembrane_current_m	*_ppvar[0]._pval
#define _p_transmembrane_current_m	_ppvar[0]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  0;
 /* external NEURON variables */
 /* declaration of user functions */
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_mea", _hoc_setdata,
 0, 0
};
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 0,0
};
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.5.0",
"mea",
 0,
 "initial_part_line0_mea",
 "initial_part_line1_mea",
 "initial_part_line2_mea",
 "initial_part_line3_mea",
 "initial_part_line4_mea",
 "initial_part_line5_mea",
 "initial_part_line6_mea",
 "initial_part_line7_mea",
 "initial_part_line8_mea",
 "initial_part_line9_mea",
 "initial_part_line10_mea",
 "initial_part_line11_mea",
 "initial_part_line12_mea",
 "initial_part_line13_mea",
 "initial_part_line14_mea",
 "initial_part_line15_mea",
 "mea_line0_mea",
 "mea_line1_mea",
 "mea_line2_mea",
 "mea_line3_mea",
 "mea_line4_mea",
 "mea_line5_mea",
 "mea_line6_mea",
 "mea_line7_mea",
 "mea_line8_mea",
 "mea_line9_mea",
 "mea_line10_mea",
 "mea_line11_mea",
 "mea_line12_mea",
 "mea_line13_mea",
 "mea_line14_mea",
 "mea_line15_mea",
 0,
 0,
 "transmembrane_current_m_mea",
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 33, _prop);
 	/*initialize range parameters*/
 	_prop->param = _p;
 	_prop->param_size = 33;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 1, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _mea_reg() {
	int _vectorized = 0;
  _initlists();
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
  hoc_register_prop_size(_mechtype, 33, 1);
  hoc_register_dparam_semantics(_mechtype, 0, "pointer");
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 mea /home/afonso/Projects/MetaCell/InfraHNN/HNN-UI/hnn_ui/mod/x86_64/mea.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}

static void initmodel() {
  int _i; double _save;_ninits++;
{

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel();
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{
} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
 {
   mea_line0 = transmembrane_current_m * initial_part_line0 * 1e-1 ;
   mea_line1 = transmembrane_current_m * initial_part_line1 * 1e-1 ;
   mea_line2 = transmembrane_current_m * initial_part_line2 * 1e-1 ;
   mea_line3 = transmembrane_current_m * initial_part_line3 * 1e-1 ;
   mea_line4 = transmembrane_current_m * initial_part_line4 * 1e-1 ;
   mea_line5 = transmembrane_current_m * initial_part_line5 * 1e-1 ;
   mea_line6 = transmembrane_current_m * initial_part_line6 * 1e-1 ;
   mea_line7 = transmembrane_current_m * initial_part_line7 * 1e-1 ;
   mea_line8 = transmembrane_current_m * initial_part_line8 * 1e-1 ;
   mea_line9 = transmembrane_current_m * initial_part_line9 * 1e-1 ;
   mea_line10 = transmembrane_current_m * initial_part_line10 * 1e-1 ;
   mea_line11 = transmembrane_current_m * initial_part_line11 * 1e-1 ;
   mea_line12 = transmembrane_current_m * initial_part_line12 * 1e-1 ;
   mea_line13 = transmembrane_current_m * initial_part_line13 * 1e-1 ;
   mea_line14 = transmembrane_current_m * initial_part_line14 * 1e-1 ;
   mea_line15 = transmembrane_current_m * initial_part_line15 * 1e-1 ;
   }
}}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}
