import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterOutlet } from '@angular/router';
interface Selector {
  key: string;
  value: string;
}

interface ResultResponse {
  [key: string]: string;
}
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})


export class AppComponent {
  title = 'web-scraper';



  url: string = '';
  selectors: Selector[] = [];
  loading: boolean = false;
  error: string | null = null;
  result: ResultResponse | null = null;

  constructor(private http: HttpClient) { }

  addSelector() {
    this.selectors.push({ key: '', value: '' });
  }

  removeSelector(index: number) {
    this.selectors.splice(index, 1);
  }
  scrape() {
    this.loading = true;
    this.error = null;
    this.result = null;
    const selectorObj: { [key: string]: string } = {};
    this.selectors.forEach(selector => {
      if (selector.key && selector.value) {
        selectorObj[selector.key] = selector.value;
      }
    })
    console.log(selectorObj);
    this.http.post('http://localhost:5000/api/scrape', { url: this.url, selectors: selectorObj }).subscribe({
      next: (response) => {
        this.result = response as ResultResponse;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message;
        this.loading = false;
      }
    })

  }

}
