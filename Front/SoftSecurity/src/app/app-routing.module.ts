import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SoftsecurityComponent } from './softsecurity/softsecurity.component';
import { AlertaDetailComponent } from './alerta-detail/alerta-detail.component';


const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'detail/:id', component: AlertaDetailComponent },
  { path: 'alertas', component: SoftsecurityComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})

export class AppRoutingModule {}



