import sys
import os
import re
import glob
exec(open("./MIDIData.py",encoding='utf-8').read())

# volume magnification for each program
VolMul = [1.0]*128
VolMul[8] = 0.8
VolMul[24] = 0.8
VolMul[25] = 0.85
VolMul[45] = 0.8
VolMul[50] = 0.85
VolMul[73] = 0.5
VolMul[79] = 0.8
VolMul[89] = 0.75
VolMul[120] = 0.7
VolMul[121] = 0.0

# key transpose for each program
KeyChg = [0]*128

# PrgChg fix per song
#    0-127 : normal map
#  128-    : drum key(+128)
PrgChg = {}
PrgChg['MORNING_CIKYU'] = [121]*64
PrgChg['MORNING_CIKYU'][2] = 45
PrgChg['MORNING_CIKYU'][15] = 48
PrgChg['MORNING_CIKYU'][17] = 89
PrgChg['MORNING_CIKYU'][34] = 8
PrgChg['MORNING_CIKYU'][35] = 12
PrgChg['MORNING_CIKYU'][36] = 0
PrgChg['MORNING_CIKYU'][37] = 50
PrgChg['MORNING_SELF'] = [121]*64
PrgChg['MORNING_SELF'][2] = 45
PrgChg['MORNING_SELF'][14] = 73
PrgChg['MORNING_SELF'][23] = 12
PrgChg['MORNING_SELF'][25] = 50
PrgChg['MORNING_SELF'][28] = 77
PrgChg['MORNING_SELF'][34] = 8
PrgChg['MORNING_SELF'][36] = 0
PrgChg['MORNING_YOHOU'] = [121]*64
PrgChg['MORNING_YOHOU'][2] = 45
PrgChg['MORNING_YOHOU'][16] = 4
PrgChg['MORNING_YOHOU'][18] = 79
PrgChg['MORNING_YOHOU'][34] = 8
PrgChg['MORNING_YOHOU'][37] = 50
PrgChg['NIGHT_CIKYU'] = [121]*64
PrgChg['NIGHT_CIKYU'][15] = 48
PrgChg['NIGHT_CIKYU'][17] = 89
PrgChg['NIGHT_CIKYU'][18] = 79
PrgChg['NIGHT_SELF'] = [121]*64
PrgChg['NIGHT_SELF'][13] = 120
PrgChg['NIGHT_SELF'][20] = 33
PrgChg['NIGHT_SELF'][26] = 24
PrgChg['NIGHT_SELF'][33] = 25
PrgChg['NIGHT_SELF'][36] = 0
PrgChg['NIGHT_YOHOU'] = [121]*64
PrgChg['NIGHT_YOHOU'][15] = 48
PrgChg['NIGHT_YOHOU'][16] = 4
PrgChg['OPTION'] = [121]*64
PrgChg['OPTION'][16] = 4
PrgChg['OPTION'][18] = 79

# loop info(beat)
Loop = {}
Loop['MORNING_CIKYU'] = [-1,-1]
Loop['MORNING_SELF'] = [-1,-1]
Loop['MORNING_YOHOU'] = [-1,-1]
Loop['NIGHT_CIKYU'] = [-1,-1]
Loop['NIGHT_SELF'] = [-1,-1]
Loop['NIGHT_YOHOU'] = [-1,-1]
Loop['OPTION'] = [-1,-1]

# find src
if os.path.isdir('./wii/rev_wtr/'):
	filepath = './wii/rev_wtr/'
elif os.path.isdir('./jaiseq/rev_wtr/'):
	filepath = './jaiseq/rev_wtr/'
elif os.path.isdir('./rev_wtr/'):
	filepath = './rev_wtr/'
else:
	os._exit(0)

pDrumTrack = None
files = glob.glob(filepath+"*.mid")
for file in files[:]:
	if file[-7:] != '_GM.mid':
		file = re.sub('.+\\\\', '', file)
		sid = '_'.join(os.path.basename(file).split('_')[2:4]).split('.')[0]
		pMIDIData = MIDIData_LoadFromSMF(filepath+file)
		pMIDITrack = MIDIData_GetFirstTrack(pMIDIData)
		trk = 0
		lstDel = []
		while pMIDITrack:
			pMIDIEvent = MIDITrack_GetFirstEvent(pMIDITrack)
			while pMIDIEvent:
				MIDIEvent_Combine(pMIDIEvent)
				if MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_PROGRAMCHANGE:
					if PrgChg[sid][MIDIEvent_GetNumber(pMIDIEvent)] != 128:
						Prg = PrgChg[sid][MIDIEvent_GetNumber(pMIDIEvent)]
						MIDIEvent_SetNumber(pMIDIEvent,Prg)
				elif MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_CONTROLCHANGE and MIDIEvent_GetNumber(pMIDIEvent) == 7:
					if Prg < 128:
						MIDIEvent_SetValue(pMIDIEvent,int((MIDIEvent_GetValue(pMIDIEvent))*VolMul[Prg]))
				elif MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_NOTEON:
					if Prg < 128:
						MIDIEvent_SetKey(pMIDIEvent,MIDIEvent_GetKey(pMIDIEvent)+KeyChg[Prg])
						MIDIEvent_SetVelocity(pMIDIEvent,int(MIDIEvent_GetVelocity(pMIDIEvent)/4+95))
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
