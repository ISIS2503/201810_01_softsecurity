import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FalloComponent } from './fallo.component';

describe('FalloComponent', () => {
  let component: FalloComponent;
  let fixture: ComponentFixture<FalloComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FalloComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FalloComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
