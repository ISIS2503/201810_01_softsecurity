import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SoftsecurityComponent } from './softsecurity.component';

describe('SoftsecurityComponent', () => {
  let component: SoftsecurityComponent;
  let fixture: ComponentFixture<SoftsecurityComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SoftsecurityComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SoftsecurityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
