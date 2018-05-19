import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SoftsecurityComponent } from './softsecurity/softsecurity.component';

import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './/app-routing.module';
import { MapaComponent } from './mapa/mapa.component';
import { AlertaComponent } from './alerta/alerta.component';
import { FalloComponent } from './fallo/fallo.component';

@NgModule({
  declarations: [
    AppComponent,
    SoftsecurityComponent,
    MapaComponent,
    AlertaComponent,
    FalloComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [ ],
  bootstrap: [AppComponent]
})
export class AppModule { }
