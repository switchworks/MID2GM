import sys
import os
import re
import glob
exec(open("./MIDIData.py",encoding='utf-8').read())

# volume magnification for each program
VolMul = [1.0]*128
VolMul[28] = 0.7
VolMul[121] = 0.0

# key transpose for each program
KeyChg = [0]*128
KeyChg[7] = -12
KeyChg[27] = -12
KeyChg[28] = -12
KeyChg[33] = -12
KeyChg[78] = 12

# PrgChg fix per song
#    0-127 : normal map
#  128-    : drum key(+128)
PrgChg = {}
PrgChg['dolpic'] = list(range(0,128)) #[121]*128
PrgChg['dolpic'][32] = 26
PrgChg['dolpic'][33] = 34
PrgChg['dolpic'][120] = 128+60
PrgChg['mare_sea'] = list(range(0,128))
PrgChg['mare_sea'][20] = 46
PrgChg['mare_sea'][21] = 73
PrgChg['mare_sea'][22] = 89
PrgChg['mare_sea'][25] = 121
PrgChg['bianco'] = list(range(0,128))
PrgChg['bianco'][46] = 45
PrgChg['bianco'][47] = 46
PrgChg['bianco'][71] = 70
PrgChg['bianco'][72] = 71
PrgChg['bianco'][74] = 72
PrgChg['bianco'][120] = 128+60
PrgChg['bianco'][125] = 128+54
PrgChg['bianco'][126] = 128+62
PrgChg['rico'] = [121]*128#list(range(0,128))
PrgChg['rico'][8] = 7
PrgChg['rico'][18] = 18
PrgChg['rico'][28] = 27
PrgChg['rico'][29] = 28
PrgChg['rico'][34] = 33
PrgChg['rico'][68] = 66
PrgChg['rico'][79] = 78
PrgChg['rico'][100] = 128+0
PrgChg['rico'][120] = 128+60
PrgChg['rico'][121] = 67

# loop info(beat)
Loop = {}
Loop['dolpic'] = [23,207] #[19.7125,177.427]
Loop['mare_sea'] = [17,93]
Loop['bianco'] = [3.5,99.5]
Loop['rico'] = [1.5,153.5]

# resolution table(before/after)
ResChg = {}
ResChg['dolpic'] = [7,6]
ResChg['mare_sea'] = [2,3]
ResChg['bianco'] = [13,20]
ResChg['rico'] = [2,3]

# find src
if os.path.isdir('./wii/sms/'):
	filepath = './wii/sms/'
elif os.path.isdir('./jaiseq/sms/'):
	filepath = './jaiseq/sms/'
elif os.path.isdir('./sms/'):
	filepath = './sms/'
else:
	os._exit(0)

files = glob.glob(filepath+"*.mid")
for file in files[:]:
	if file[-7:] != '_GM.mid':
		file = re.sub('.+\\\\', '', file)
		sid = os.path.splitext(os.path.basename(file))[0].split('_',1)[1].split('.')[0]
		pMIDIData = MIDIData_LoadFromSMF(filepath+file)
		if sid == 'ico':
 			MIDIData_SaveAsMIDICSV(pMIDIData,filepath+file+'.csv')
		pDrumTrack = None
		pYoshiTrack = None
		pMIDITrack = MIDIData_GetFirstTrack(pMIDIData)
		trk = 0
		lstDel = []
		while pMIDITrack:
			Prg=-1
			pMIDIEvent = MIDITrack_GetFirstEvent(pMIDITrack)
			while pMIDIEvent:
				MIDIEvent_Combine(pMIDIEvent)
				if MIDIEvent_IsProgramChange(pMIDIEvent):
					Prg = PrgChg[sid][MIDIEvent_GetNumber(pMIDIEvent)]
					if PrgChg[sid][MIDIEvent_GetNumber(pMIDIEvent)] < 128:
						MIDIEvent_SetNumber(pMIDIEvent,Prg)
					else:
						lstDel += [pMIDIEvent]
				elif MIDIEvent_IsTempo(pMIDIEvent):
					MIDIEvent_SetTempo(pMIDIEvent,int(MIDIEvent_GetTempo(pMIDIEvent)*ResChg[sid][1]/ResChg[sid][0]))
				elif MIDIEvent_IsControlChange(pMIDIEvent):
					if MIDIEvent_GetNumber(pMIDIEvent) == 7:
						if Prg < 128:
							MIDIEvent_SetValue(pMIDIEvent,int((MIDIEvent_GetValue(pMIDIEvent))*VolMul[Prg]))
				elif MIDIEvent_IsNoteOn(pMIDIEvent):
					if Prg < 128:
						MIDIEvent_SetKey(pMIDIEvent,MIDIEvent_GetKey(pMIDIEvent)+KeyChg[Prg])
					else:
						pDrumEvent = MIDIEvent_CreateClone(pMIDIEvent)
						MIDIEvent_SetChannel(pDrumEvent,9)
						if Prg==128+60: # yoshi bongo
							if pYoshiTrack is None:
								pYoshiTrack = MIDITrack_Create()
							if MIDIEvent_GetKey(pMIDIEvent)==62: #
								MIDIEvent_SetKey(pDrumEvent,61)
							elif MIDIEvent_GetKey(pMIDIEvent)==63: #
								MIDIEvent_SetKey(pDrumEvent,60)
							MIDITrack_InsertEvent(pYoshiTrack,pDrumEvent)
						else:
							if pDrumTrack is None:
								pDrumTrack = MIDITrack_Create()
							if Prg==128+0: # rico?
								pass
							elif Prg==128+54: # tambourine
								MIDIEvent_SetKey(pDrumEvent,54)
							elif Prg==128+62: # conga
								if MIDIEvent_GetKey(pMIDIEvent)==36: #
									MIDIEvent_SetKey(pDrumEvent,64)
								elif MIDIEvent_GetKey(pMIDIEvent)==43: #
									MIDIEvent_SetKey(pDrumEvent,63)
								elif MIDIEvent_GetKey(pMIDIEvent)==41: #
									MIDIEvent_SetKey(pDrumEvent,56)
								elif MIDIEvent_GetKey(pMIDIEvent)==42: #
									MIDIEvent_SetKey(pDrumEvent,62)
							MIDITrack_InsertEvent(pDrumTrack,pDrumEvent)
						lstDel += [pMIDIEvent]
				pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
			if lstDel != []:
				for eDel in lstDel:
					MIDIEvent_Delete(eDel)
				lstDel = []
			trk+=1
			pMIDITrack = MIDITrack_GetNextTrack(pMIDITrack)
		if Loop[sid] != [-1,-1]:
			MIDITrack_InsertMarker(MIDIData_GetFirstTrack(pMIDIData),int(Loop[sid][0]*MIDIData_GetTimeResolution(pMIDIData)*ResChg[sid][1]/ResChg[sid][0]),'loopStart')
			MIDITrack_InsertMarker(MIDIData_GetFirstTrack(pMIDIData),int(Loop[sid][1]*MIDIData_GetTimeResolution(pMIDIData)*ResChg[sid][1]/ResChg[sid][0]),'loopEnd')
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
		if not pDrumTrack is None:
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
		if not pYoshiTrack is None:
			MIDIData_SaveAsSMF(pMIDIData,filepath+sid+'_GM.mid')
			with open(filepath+sid+'_GM.mid', 'r+b') as f:
				b = bytearray(f.read())
				b[0x0D] = int(b[0x0D]*ResChg[sid][1]/ResChg[sid][0])
				f.seek(0)
				f.write(b)
			MIDITrack_InsertEndofTrack(pYoshiTrack,MIDIEvent_GetTime(MIDITrack_GetLastEvent(pYoshiTrack)))
			MIDIData_AddTrack(pMIDIData,pYoshiTrack)
			fn = filepath+sid+'y_GM.mid'
		else:
			fn = filepath+sid+'_GM.mid'
		MIDIData_SaveAsSMF(pMIDIData,fn)
		with open(fn, 'r+b') as f:
			b = bytearray(f.read())
			b[0x0D] = int(b[0x0D]*ResChg[sid][1]/ResChg[sid][0])
			f.seek(0)
			f.write(b)
		MIDIData_Delete(pMIDIData)
		pDrumTrack = None
