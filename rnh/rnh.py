import sys
import os
import re
import glob
exec(open("./MIDIData.py",encoding='utf-8').read())

# volume magnification for each program
VolMul = [1.0]*128
VolMul[5] = 0.8
VolMul[8] = 0.85
VolMul[18] = 0.8
VolMul[29] = 0.75
VolMul[30] = 0.65
VolMul[39] = 0.7
VolMul[46] = 0.65
VolMul[48] = 0.8
VolMul[55] = 0.7
VolMul[58] = 0.7
VolMul[60] = 1.2
VolMul[73] = 0.8
VolMul[81] = 0.7
VolMul[104] = 0.8
VolMul[121] = 0.0

# key transpose for each program
KeyChg = [0]*128
KeyChg[1] = -24
KeyChg[6] = -24
KeyChg[18] = 0
KeyChg[24] = -12
KeyChg[29] = -12
KeyChg[30] = -24
KeyChg[33] = -24
KeyChg[36] = -24
KeyChg[37] = -12
KeyChg[38] = -24
KeyChg[41] = -12
KeyChg[42] = -24
KeyChg[47] = -24
KeyChg[55] = -24
KeyChg[61] = 12
KeyChg[104] = -12

# PrgChg fix per song
#    0-127 : normal map
#  128-    : drum key(+128)
PrgChg = {}
PrgChg['01'] = [121]*32 + [48,46,48]
PrgChg['02'] = [121]*32 + [48,46,54,73,128+49,1,60,47,128+38]
PrgChg['02'][7] = 5
PrgChg['03'] = [121]*32 + [30,15,54,33,47,128+49,128+42,128+38,128+36]
PrgChg['04'] = [121]*32 + [48,48,47,128+49]
PrgChg['05a'] = [121]*32 + [128+38,47,128+49,48,60,121,68,57,45,42]
PrgChg['05b'] = [121]*32 + [54,48,45,73,11,42]
PrgChg['06a'] = [121]*32 + [48,60,54,46,47,128+49,48]
PrgChg['06b'] = [121]*32 + [73,24,32,52,41]
PrgChg['07a'] = [121]*32 + [48,128+36,73,46,128+49]
PrgChg['07b'] = [121]*32 + [22,48,46,121,128+36,128+70,128+41,128+54]
PrgChg['08a'] = [121]*32 + [73,128+49,45,60,46,48,121,68,47,128+38]
PrgChg['08b'] = [121]*32 + [24,45,11,32,128+69,128+54,128+62]
PrgChg['09'] = [121]*32 + [60,48,73,128+49,47,58,57]
PrgChg['10'] = [121]*32 + [46,32,61,57,48,60,47,128+38,128+49]
PrgChg['11'] = [121]*32 + [37,15,61,53,33,128+49,128+42,128+36,128+38,128+41,55]
PrgChg['12'] = [121]*18 + [8] + [121]*13 + [73,48,81,36,128+36,128+38,128+41,128+42,128+49]
PrgChg['13'] = [121]*32 + [48,46,11]
PrgChg['14'] = [121]*32 + [128+36,128+38,128+49,48,60,14,56]
PrgChg['15'] = [121]*32 + [48,48,11,5]
PrgChg['16'] = [121]*32 + [54,121,78,121,128+75,128+54]
PrgChg['17'] = [121]*32 + [56,11,48,60,128+38,128+49,121]
PrgChg['18'] = [121]*32 + [46,38,48,128+36,128+69,128+41,128+75]
PrgChg['19'] = [121]*32 + [48,68,33,128+36,128+38]
PrgChg['20'] = [121]*32 + [48,68,13,45,73]
PrgChg['21'] = [121]*32 + [48,73,33,104,121,47,128+64,54]
PrgChg['22'] = [121]*32 + [46,39,54,128+64,116,128+69,128+70]
PrgChg['23'] = [121]*32 + [8,46,48,0,128+49]
PrgChg['24'] = [121]*32 + [73,32,24,48,128+37,128+36,128+54]
PrgChg['25'] = [121]*32 + [128+36,128+38,128+42,128+49,128+41,81,48,57,33,55]
PrgChg['26'] = [121]*32 + [30,81,18,33,128+49,128+42,128+36,128+38,128+41]
PrgChg['27'] = [121]*32 + [128+36,128+38,128+56,128+49,128+41,53,33,18,58,48,29,30]
PrgChg['28'] = [121]*16 + [81] + [121]*15 + [29,48,33,128+49,128+42,128+36,128+38,128+41,30,30]
PrgChg['29'] = [121]*32 + [48,29,53,33,128+42,128+49,128+36,128+38,128+41,30,0]
PrgChg['30'] = [121]*32 + [30,60,58,48,33,128+42,128+38,128+36,128+41,128+49]
PrgChg['31'] = [121]*32 + [48,56,128+49,128+36,128+38,33,14]
PrgChg['32'] = [121]*32 + [54,116,38,128+36,128+38]
PrgChg['33'] = [121]*32 + [128+38,47,128+49,48,121,73,57,60]
PrgChg['34'] = [121]*32 + [48,60,56,14,47,128+38,128+49]
PrgChg['35'] = [121]*32 + [128+36,128+38,128+42,128+49,128+41,33,53,38,104,45]
PrgChg['36'] = [121]*32 + [48,54,104,48,128+49,128+36,128+38,128+82,128+61,68]
PrgChg['37'] = [121]*32 + [48,46,48,53,14]
PrgChg['38'] = [121]*32 + [60,48,128+49,47,48]
PrgChg['39'] = [121]*32 + [54,1,126]
PrgChg['40'] = [121]*32 + [19,54,1]
PrgChg['41'] = [121]*32 + [48,1,54]
PrgChg['42'] = [121]*32 + [81,54,48,33,128+49,128+42,128+36,128+38,128+41]
PrgChg['43'] = [121]*32 + [54,121,121,6,121,38,128+36,128+38,128+41,128+42,128+49]
PrgChg['44'] = [121]*32 + [54,46,60,48,47,33,128+49]
PrgChg['45'] = [121]*32 + [60,87,48,11,128+36,47,128+38,33]
PrgChg['46'] = [121]*32 + [48,60,47,121,33]
PrgChg['47'] = [121]*32 + [71,73,68,32,128+61,128+56,128+82,128+42]
PrgChg['48'] = [121]*32 + [68,55,48,12,33,128+36,128+38,121,128+42,128+49]
PrgChg['49'] = [121]*32 + [48,11,68,48]
PrgChg['50'] = [121]*32 + [54,48,11,73,47,121,128+49]
PrgChg['51'] = [121]*32 + [54,46,48,33,30,116,128+59,1,128+49,0]
PrgChg['52'] = [121]*32 + [54,1,48,30,30,128+49,19,128+36]
PrgChg['53'] = [121]*32 + [30,48,48,128+41,128+64,128+69,128+54,128+56,128+38]
PrgChg['54'] = [121]*32 + [58,48,30,33,47,128+49,128+42,128+38,128+36,128+41]
PrgChg['55'] = [121]*32 + [57,48,30,33,18,128+49,128+42,128+38,128+36,128+41,29,128+56]
PrgChg['56'] = [121]*32 + [11,48]
PrgChg['57a'] = [121]*32 + [81,48,30,33,128+49,128+42,128+38,128+36,128+41]
PrgChg['57b'] = [121]*32 + [81,48,30,33,128+49,128+42,128+38,128+36,128+41]
PrgChg['57b'][17] = 46
PrgChg['58a'] = [121]*32 + [48,46,121,73,128+49,60,128+36,128+38]
PrgChg['58b'] = [121]*32 + [48,57,48,73,46,128+36,128+38,128+49]

# loop info(beat)
Loop = {}
Loop['01'] = [0,192]
Loop['02'] = [-1,-1]
Loop['03'] = [0,191]
Loop['04'] = [0,128]
Loop['05a'] = [64,160]
Loop['05b'] = [0,96]
Loop['06a'] = [0,128]
Loop['06b'] = [0.5,96.5]
Loop['07a'] = [1.5,169.5]
Loop['07b'] = [0,68]
Loop['08a'] = [33,157]
Loop['08b'] = [1,81]
Loop['09'] = [0,88]
Loop['10'] = [0,160]
Loop['11'] = [16,72]
Loop['12'] = [31.6666,159.6666]
Loop['13'] = [0,144]
Loop['14'] = [0,128]
Loop['15'] = [3,195]
Loop['16'] = [0,72]
Loop['17'] = [1,97]
Loop['18'] = [0,120]
Loop['19'] = [1,52]
Loop['20'] = [0,96]
Loop['21'] = [0,88]
Loop['22'] = [1,97]
Loop['23'] = [0,200]
Loop['24'] = [0,144]
Loop['25'] = [8,104]
Loop['26'] = [16,144]
Loop['27'] = [4,100]
Loop['28'] = [32.5,128.5]
Loop['29'] = [2,66]
Loop['30'] = [4,116]
Loop['31'] = [1,97]
Loop['32'] = [0,24]
Loop['33'] = [2,110]
Loop['34'] = [0,116]
Loop['35'] = [8,116]
Loop['36'] = [0,168]
Loop['37'] = [1,97]
Loop['38'] = [0,160]
Loop['39'] = [0,24]
Loop['40'] = [0,96]
Loop['41'] = [0,128]
Loop['42'] = [4,100]
Loop['43'] = [0,96]
Loop['44'] = [4,172]
Loop['45'] = [0,250]
Loop['46'] = [0,180]
Loop['47'] = [0,106]
Loop['48'] = [0,96]
Loop['49'] = [0,68]
Loop['50'] = [0,64]
Loop['51'] = [0,224]
Loop['52'] = [170,194]
Loop['53'] = [0,136]
Loop['54'] = [35,171]
Loop['55'] = [80,208]
Loop['56'] = [0,192]
Loop['57a'] = [-1,-1]
Loop['57b'] = [-1,-1]
Loop['58a'] = [0,276]
Loop['58b'] = [0,88]

# find src
if os.path.isdir('./snes/rnh/'):
	filepath = './snes/rnh/'
elif os.path.isdir('./spc/rnh/'):
	filepath = './spc/rnh/'
elif os.path.isdir('./rnh/'):
	filepath = './rnh/'
else:
	os._exit(0)


DrumVolMul = 1.0
pDrumTrack = None
files = glob.glob(filepath+"*.mid")
for file in files[:]:
	if file[-7:] != '_GM.mid':
		file = re.sub('.+\\\\', '', file)
		sid = os.path.splitext(os.path.basename(file))[0].split('_')[0]
		pMIDIData = MIDIData_LoadFromSMF(filepath+file)
		pMIDITrack = MIDIData_GetFirstTrack(pMIDIData)
		vol=-1
		lstDel = []
		while pMIDITrack:
			pMIDIEvent = MIDITrack_GetFirstEvent(pMIDITrack)
			while pMIDIEvent:
				if MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_CONTROLCHANGE and MIDIEvent_GetNumber(pMIDIEvent) == 7:
					vol=MIDIEvent_GetValue(pMIDIEvent)
					lstDel += [pMIDIEvent]
				elif MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_CONTROLCHANGE and MIDIEvent_GetNumber(pMIDIEvent) == 11:
					MIDIEvent_SetNumber(pMIDIEvent,7)
					MIDIEvent_SetValue(pMIDIEvent,int((MIDIEvent_GetValue(pMIDIEvent)*vol)/127))
				pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
			if lstDel != []:
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			pMIDITrack = MIDITrack_GetNextTrack(pMIDITrack)
		pMIDITrack = MIDIData_GetFirstTrack(pMIDIData)
		trk = 0
		lstDel = []
		while pMIDITrack:
			pMIDIEvent = MIDITrack_GetFirstEvent(pMIDITrack)
			while pMIDIEvent:
				MIDIEvent_Combine(pMIDIEvent)
				if MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_PROGRAMCHANGE:
					Prg = PrgChg[sid][MIDIEvent_GetNumber(pMIDIEvent)]
					if PrgChg[sid][MIDIEvent_GetNumber(pMIDIEvent)] < 128:
						MIDIEvent_SetNumber(pMIDIEvent,Prg)
					else:
						lstDel += [pMIDIEvent]
				elif MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_CONTROLCHANGE and MIDIEvent_GetNumber(pMIDIEvent) == 7:
					if Prg < 128:
						MIDIEvent_SetValue(pMIDIEvent,int((MIDIEvent_GetValue(pMIDIEvent)+127/2)*VolMul[Prg]))
					else:
						DrumVolMul = int(MIDIEvent_GetValue(pMIDIEvent))
						lstDel += [pMIDIEvent]
				elif MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_CONTROLCHANGE and MIDIEvent_GetNumber(pMIDIEvent) == 10:
					if Prg >= 128:
						if pDrumTrack == None:
							pDrumTrack = MIDITrack_Create()
							MIDITrack_InsertProgramChange(pDrumTrack,0,9,16)
							MIDITrack_InsertControlChange(pDrumTrack,MIDIEvent_GetTime(pMIDIEvent),9,7,110)
						lstDel += [pMIDIEvent]
				elif MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_CONTROLCHANGE and MIDIEvent_GetNumber(pMIDIEvent) == 91:
					lstDel += [pMIDIEvent]
				elif MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_NOTEON:
					if Prg < 128:
						MIDIEvent_SetKey(pMIDIEvent,MIDIEvent_GetKey(pMIDIEvent)+KeyChg[Prg])
					else: # warning : drum part now incorrect
						if pDrumTrack == None:
							pDrumTrack = MIDITrack_Create()
							MIDITrack_InsertProgramChange(pDrumTrack,0,9,16)
							MIDITrack_InsertControlChange(pDrumTrack,MIDIEvent_GetTime(pMIDIEvent),9,7,110)
						pDrumEvent = MIDIEvent_CreateClone(pMIDIEvent)
						MIDIEvent_SetVelocity(pDrumEvent,int(MIDIEvent_GetVelocity(pMIDIEvent)*DrumVolMul/127))
						MIDIEvent_SetChannel(pDrumEvent,9)
						if Prg==128+41: # tom
							MIDIEvent_SetKey(pDrumEvent,MIDIEvent_GetKey(pMIDIEvent)-24)
						elif Prg==128+42: # hat
							if MIDIEvent_GetKey(pMIDIEvent)==72: #close
								MIDIEvent_SetKey(pDrumEvent,42)
							elif MIDIEvent_GetKey(pMIDIEvent)==73: #pedal
								MIDIEvent_SetKey(pDrumEvent,44)
							elif MIDIEvent_GetKey(pMIDIEvent)==74: #open?
								MIDIEvent_SetKey(pDrumEvent,46)
							elif MIDIEvent_GetKey(pMIDIEvent)==82: #open?
								MIDIEvent_SetKey(pDrumEvent,46)
							if sid=='12' and DrumVolMul == 71:
								MIDIEvent_SetKey(pDrumEvent,46)
							if sid=='54' and MIDIEvent_GetDuration(pMIDIEvent)==22:
								MIDIEvent_SetKey(pDrumEvent,46)
							MIDIEvent_SetVelocity(pDrumEvent,int(MIDIEvent_GetVelocity(pDrumEvent)+30))
						elif Prg==128+49: # crash
							if MIDIEvent_GetKey(pMIDIEvent)==72: #crash
								MIDIEvent_SetKey(pDrumEvent,49)
							elif MIDIEvent_GetKey(pMIDIEvent)==81: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							elif MIDIEvent_GetKey(pMIDIEvent)==83: #crash
								MIDIEvent_SetKey(pDrumEvent,59)
							elif MIDIEvent_GetKey(pMIDIEvent)==76: #crash
								MIDIEvent_SetKey(pDrumEvent,52)
							elif MIDIEvent_GetKey(pMIDIEvent)==79: #crash
								MIDIEvent_SetKey(pDrumEvent,55)
							elif MIDIEvent_GetKey(pMIDIEvent)==71: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							elif MIDIEvent_GetKey(pMIDIEvent)==73: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							elif MIDIEvent_GetKey(pMIDIEvent)==74: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							elif MIDIEvent_GetKey(pMIDIEvent)==75: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							elif MIDIEvent_GetKey(pMIDIEvent)==43: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							elif MIDIEvent_GetKey(pMIDIEvent)==60: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							elif MIDIEvent_GetKey(pMIDIEvent)==65: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							elif MIDIEvent_GetKey(pMIDIEvent)==69: #crash
								MIDIEvent_SetKey(pDrumEvent,57)
							MIDIEvent_SetVelocity(pDrumEvent,int(MIDIEvent_GetVelocity(pDrumEvent)+30))
						elif Prg==128+75: # 
							MIDIEvent_SetKey(pDrumEvent,75)
							MIDIEvent_SetVelocity(pDrumEvent,int(MIDIEvent_GetVelocity(pDrumEvent)+30))
						elif Prg==128+64: # 
							if MIDIEvent_GetKey(pDrumEvent) == 61:
								MIDIEvent_SetKey(pDrumEvent,64)
							elif MIDIEvent_GetKey(pDrumEvent) == 82:
								MIDIEvent_SetKey(pDrumEvent,62)
							elif MIDIEvent_GetKey(pDrumEvent) == 64:
								MIDIEvent_SetKey(pDrumEvent,63)
							MIDIEvent_SetVelocity(pDrumEvent,int(MIDIEvent_GetVelocity(pDrumEvent)+30))
						else:
							MIDIEvent_SetKey(pDrumEvent,Prg-128)
							MIDIEvent_SetVelocity(pDrumEvent,int(MIDIEvent_GetVelocity(pDrumEvent)+30))
						MIDITrack_InsertEvent(pDrumTrack,pDrumEvent)
						lstDel += [pMIDIEvent]
				elif MIDIEvent_GetKind(pMIDIEvent) == MIDIEVENT_SYSEXSTART:
						lstDel += [pMIDIEvent]
				pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
			if lstDel != []:
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			trk+=1
			pMIDITrack = MIDITrack_GetNextTrack(pMIDITrack)
		if Loop[sid] != [-1,-1]:
			MIDITrack_InsertMarker(MIDIData_GetFirstTrack(pMIDIData),int(Loop[sid][0]*MIDIData_GetTimeResolution(pMIDIData)),'loopStart')
			MIDITrack_InsertMarker(MIDIData_GetFirstTrack(pMIDIData),int(Loop[sid][1]*MIDIData_GetTimeResolution(pMIDIData)),'loopEnd')
		if pDrumTrack != None:
			# additional for drum track
			pMIDIEvent = MIDITrack_GetFirstEvent(pDrumTrack)
			while pMIDIEvent:
				pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
			if lstDel != []:
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			MIDITrack_InsertEndofTrack(pDrumTrack,MIDIEvent_GetTime(MIDITrack_GetLastEvent(pDrumTrack)))
			MIDIData_AddTrack(pMIDIData,pDrumTrack)
			if sid=='18':
				pOchTrack = MIDITrack_Create()
				MIDITrack_InsertControlChange(pOchTrack,0,10,0,120)
				MIDITrack_InsertControlChange(pOchTrack,0,10,32,0)
				MIDITrack_InsertProgramChange(pOchTrack,0,10,25)
				pMIDIEvent = MIDITrack_GetFirstEvent(pDrumTrack)
				while pMIDIEvent:
					if MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_NOTEON:
						if MIDIEvent_GetKey(pMIDIEvent) == 75:
							pDrumEvent = MIDIEvent_CreateClone(pMIDIEvent)
							MIDIEvent_SetChannel(pDrumEvent,10)
							MIDIEvent_SetKey(pDrumEvent,50)
							MIDITrack_InsertEvent(pOchTrack,pDrumEvent)
							lstDel += [pMIDIEvent]
						if MIDIEvent_GetKey(pMIDIEvent) == 70:
							pDrumEvent = MIDIEvent_CreateClone(pMIDIEvent)
							MIDIEvent_SetChannel(pDrumEvent,10)
							MIDIEvent_SetKey(pDrumEvent,47)
							MIDITrack_InsertEvent(pOchTrack,pDrumEvent)
							lstDel += [pMIDIEvent]
						if MIDIEvent_GetKey(pMIDIEvent) == 60:
							pDrumEvent = MIDIEvent_CreateClone(pMIDIEvent)
							MIDIEvent_SetChannel(pDrumEvent,10)
							MIDIEvent_SetKey(pDrumEvent,41)
							MIDITrack_InsertEvent(pOchTrack,pDrumEvent)
							lstDel += [pMIDIEvent]
					pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
				MIDITrack_InsertEndofTrack(pOchTrack,MIDIEvent_GetTime(MIDITrack_GetLastEvent(pOchTrack)))
				MIDIData_AddTrack(pMIDIData,pOchTrack)
				pOchTrack = None
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			if sid=='02' or sid=='05a' or sid=='07a' or sid=='08a' or sid=='10' or sid=='14' or sid=='17' or sid=='19' or sid=='31' or sid=='33' or sid=='34' or sid=='45' or sid=='52' or sid=='58a' or sid=='58b':
				pOchTrack = MIDITrack_Create()
				MIDITrack_InsertControlChange(pOchTrack,0,10,0,120)
				MIDITrack_InsertControlChange(pOchTrack,0,10,32,0)
				MIDITrack_InsertProgramChange(pOchTrack,0,10,48)
				pMIDIEvent = MIDITrack_GetFirstEvent(pDrumTrack)
				while pMIDIEvent:
					if MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_NOTEON:
						if MIDIEvent_GetKey(pMIDIEvent) == 36 or MIDIEvent_GetKey(pMIDIEvent) == 38:
							pDrumEvent = MIDIEvent_CreateClone(pMIDIEvent)
							MIDIEvent_SetChannel(pDrumEvent,10)
							MIDITrack_InsertEvent(pOchTrack,pDrumEvent)
							lstDel += [pMIDIEvent]
					pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
				MIDITrack_InsertEndofTrack(pOchTrack,MIDIEvent_GetTime(MIDITrack_GetLastEvent(pOchTrack)))
				MIDIData_AddTrack(pMIDIData,pOchTrack)
				pOchTrack = None
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
		# additional
		pMIDITrack = MIDIData_GetFirstTrack(pMIDIData)
		trk = 0
		lstDel = []
		while pMIDITrack:
			pMIDIEvent = MIDITrack_GetFirstEvent(pMIDITrack)
			while pMIDIEvent:
				pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
			if lstDel != []:
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			trk+=1
			pMIDITrack = MIDITrack_GetNextTrack(pMIDITrack)
		MIDIData_SaveAsSMF(pMIDIData,filepath+file[:-4]+'_GM.mid')
		MIDIData_Delete(pMIDIData)
		pDrumTrack = None
