import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    analyzeResume(file: File, jobDescription: string): Observable<any> {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('job_description', jobDescription);
        return this.http.post(`${this.apiUrl}/resume/analyze`, formData);
    }

    generateDocument(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/document/generate`, data);
    }

    generateResearch(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/research/generate`, data);
    }

    generateCreative(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/creative/generate`, data);
    }

    generateEmail(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/email/generate`, data);
    }

    generateSocialMedia(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/social-media/generate`, data);
    }
}
