import sys
import os
exec(open("./MIDIData.py",encoding='utf-8').read())

if len(sys.argv) < 2:
	sys.exit()
elif not sys.argv[1].endswith('.mid') or not os.path.isfile(sys.argv[1]):
	sys.exit()

pMIDIData = MIDIData_LoadFromSMF(sys.argv[1])
pMIDITrack = MIDIData_GetFirstTrack(pMIDIData)
trk = 0
while pMIDITrack:
	msg = 'Trk '+str(trk).zfill(2)+' :'
	pMIDIEvent = MIDITrack_GetFirstEvent(pMIDITrack)
	while pMIDIEvent:
		if MIDIEvent_GetKind(pMIDIEvent) >> 4 << 4 == MIDIEVENT_PROGRAMCHANGE:
			msg += ' '+str(MIDIEvent_GetNumber(pMIDIEvent)).rjust(3)
			pass#print('Trk '+str(trk).zfill(2)+' : '+str(MIDIEvent_GetNumber(pMIDIEvent)))
		pMIDIEvent = MIDIEvent_GetNextEvent(pMIDIEvent)
	print(msg)
	trk+=1
	pMIDITrack = MIDITrack_GetNextTrack(pMIDITrack)
