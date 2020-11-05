#include "Pythia8/Pythia.h"

using namespace Pythia8;

int main()
{
  Pythia pythia;
  pythia.readString("WeakSingleBoson:all = on");
  pythia.readString("PhaseSpace:pTHatMin = 20.");
  pythia.readString("Beams:eCM = 7000.");
  pythia.init();

  
  Event& event = pythia.event;
  //ParticleData particle_data;

  // Begin event loop. Generate event. Skip if error. List first one.
  for (int iEvent = 0; iEvent < 100; ++iEvent)
  {
    if (!pythia.next()) continue;

    if(event[iEvent].isFinal() and event[iEvent].isCharged())
    {
      std::cout << event[iEvent].name() << std::endl;
    }
  }
  //pythia.stat();
  return 0;
}

