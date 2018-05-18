import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SoftsecurityComponent } from './softsecurity/softsecurity.component';

import { FormsModule } from '@angular/forms';
import { AlertaDetailComponent } from './alerta-detail/alerta-detail.component';
import { AppRoutingModule } from './/app-routing.module';
import { MapaComponent } from './mapa/mapa.component';
import { AlertaComponent } from './alerta/alerta.component';
import { FalloComponent } from './fallo/fallo.component';
import { FalloDetailComponent } from './fallo-detail/fallo-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    SoftsecurityComponent,
    AlertaDetailComponent,
    MapaComponent,
    AlertaComponent,
    FalloComponent,
    FalloDetailComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
