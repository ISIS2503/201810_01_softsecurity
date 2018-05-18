import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FalloDetailComponent } from './fallo-detail.component';

describe('FalloDetailComponent', () => {
  let component: FalloDetailComponent;
  let fixture: ComponentFixture<FalloDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FalloDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FalloDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
