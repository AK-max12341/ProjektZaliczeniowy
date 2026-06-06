import {
  Component,
  OnInit,
  ChangeDetectorRef
} from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

interface CurrencyRate {
  currency: string;
  code: string;
  rate: number;
  date: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {

  years: number[] = [];
  quarters: number[] = [];
  months: number[] = [];
  days: number[] = [];

  currencies: CurrencyRate[] = [];

  selectedYear: number | null = null;
  selectedQuarter: number | null = null;
  selectedMonth: number | null = null;
  selectedDay: number | null = null;

  message: string = '';

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {

    this.http
      .get<number[]>('http://localhost:8000/years')
      .subscribe(data => {

        this.years = [...data];

        this.cdr.detectChanges();

        console.log('Lata:', data);

      });

  }

  fetchCurrencies(): void {

    this.message = 'Pobieranie danych z NBP...';

    this.http
      .post<any>(
        'http://localhost:8000/currencies/fetch',
        {}
      )
      .subscribe({
        next: (response) => {

          this.message = response.message;

          this.cdr.detectChanges();

          console.log(response);

        },
        error: (error) => {

          this.message = 'Wystąpił błąd podczas pobierania danych.';

          console.error(error);

          this.cdr.detectChanges();

        }
      });

  }

  selectYear(year: number): void {

    this.selectedYear = year;

    this.quarters = [];
    this.months = [];
    this.days = [];
    this.currencies = [];

    this.selectedQuarter = null;
    this.selectedMonth = null;
    this.selectedDay = null;

    this.http
      .get<number[]>(`http://localhost:8000/quarters/${year}`)
      .subscribe(data => {

        this.quarters = [...data];

        this.cdr.detectChanges();

        console.log('Kwartały:', data);

      });

  }

  selectQuarter(quarter: number): void {

    this.selectedQuarter = quarter;

    this.months = [];
    this.days = [];
    this.currencies = [];

    this.selectedMonth = null;
    this.selectedDay = null;

    this.http
      .get<number[]>(`http://localhost:8000/months/${this.selectedYear}`)
      .subscribe(data => {

        const quarterMonths = data.filter(month => {

          const calculatedQuarter =
            Math.floor((month - 1) / 3) + 1;

          return calculatedQuarter === quarter;

        });

        this.months = quarterMonths;

        this.cdr.detectChanges();

        console.log('Miesiące w kwartale:', quarterMonths);

      });

  }

  selectMonth(month: number): void {

    this.selectedMonth = month;

    this.days = [];
    this.currencies = [];

    this.selectedDay = null;

    this.http
      .get<number[]>(
        `http://localhost:8000/days/${this.selectedYear}/${month}`
      )
      .subscribe(data => {

        this.days = [...data];

        this.cdr.detectChanges();

        console.log('Dni:', data);

      });

  }

  selectDay(day: number): void {

    this.selectedDay = day;

    const formattedMonth =
      String(this.selectedMonth).padStart(2, '0');

    const formattedDay =
      String(day).padStart(2, '0');

    const selectedDate =
      `${this.selectedYear}-${formattedMonth}-${formattedDay}`;

    this.http
      .get<CurrencyRate[]>(
        `http://localhost:8000/currencies/${selectedDate}`
      )
      .subscribe(data => {

        this.currencies = [...data];

        this.cdr.detectChanges();

        console.log('Kursy:', data);

      });

  }

}