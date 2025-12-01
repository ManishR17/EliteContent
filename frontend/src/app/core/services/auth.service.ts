import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Router } from '@angular/router';

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private apiUrl = `${environment.apiUrl}/auth`;
    private currentUserSubject = new BehaviorSubject<any>(null);
    public currentUser$ = this.currentUserSubject.asObservable();

    constructor(private http: HttpClient, private router: Router) {
        this.loadUser();
    }

    private loadUser() {
        const token = localStorage.getItem('token');
        if (token) {
            // Ideally verify token with backend, for now just decode or assume valid
            // This is a simplified version
            this.currentUserSubject.next({ token });
        }
    }

    register(user: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/register`, user);
    }

    login(credentials: any): Observable<any> {
        const formData = new FormData();
        formData.append('username', credentials.email);
        formData.append('password', credentials.password);

        return this.http.post(`${this.apiUrl}/token`, formData).pipe(
            tap((response: any) => {
                localStorage.setItem('token', response.access_token);
                this.currentUserSubject.next({ token: response.access_token });
            })
        );
    }

    logout() {
        localStorage.removeItem('token');
        this.currentUserSubject.next(null);
        this.router.navigate(['/login']);
    }

    getToken(): string | null {
        return localStorage.getItem('token');
    }

    isAuthenticated(): boolean {
        return !!this.getToken();
    }
}
