import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlertaDetailComponent } from './alerta-detail.component';

describe('AlertaDetailComponent', () => {
  let component: AlertaDetailComponent;
  let fixture: ComponentFixture<AlertaDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlertaDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlertaDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
