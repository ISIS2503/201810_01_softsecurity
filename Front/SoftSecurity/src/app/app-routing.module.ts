import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SoftsecurityComponent } from './softsecurity/softsecurity.component';


const routes: Routes = [
  { path: 'alertas', component: SoftsecurityComponent },
  { path: 'mapa', component: SoftsecurityComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})

export class AppRoutingModule {}



