{
  c1 = new TCanvas("c1","c1",200,10,700,700);
                                                                                
  int n = 20;
  TH1F* nom = new TH1F("nom", "nom", n, 0, 1);
                                                                                
  TRandom3* rd = new TRandom3();
                                                                                
  for (int j = 1; j <= n; ++j) {
    nom->SetBinContent(j, rd->Rndm()-0.5);
    nom->SetBinError(j, 0.5);
  }
                                                                                
  TH1F* envHi = new TH1F("envhi", "envhi", n, 0, 1);
  TH1F* envLo = new TH1F("envhi", "envhi", n, 0, 1);
  for (int j = 1; j <= n; ++j) {
    double y = nom->GetBinContent(j);
    double ey = nom->GetBinError(j);
    envHi->SetBinContent(j, y+ey);
    envLo->SetBinContent(j, y-ey);
  }
                                                                                
  nom->SetMinimum(-2);
  nom->SetMaximum(2);
  nom->Draw("");
  envHi->SetFillColor(2);
  envHi->Draw("same");
  //envLo->SetFillColor(2);
  //envLo->Draw("same");
  nom->Draw("same");
}
