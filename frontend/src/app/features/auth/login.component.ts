import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, FormsModule, RouterModule],
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent {
    credentials = {
        email: '',
        password: ''
    };
    isLoading = false;
    error = '';

    constructor(private authService: AuthService, private router: Router) { }

    onSubmit() {
        if (!this.credentials.email || !this.credentials.password) {
            this.error = 'Please enter email and password';
            return;
        }

        this.isLoading = true;
        this.error = '';

        this.authService.login(this.credentials).subscribe({
            next: () => {
                this.router.navigate(['/dashboard']);
            },
            error: (err) => {
                this.error = 'Invalid email or password';
                this.isLoading = false;
                console.error(err);
            }
        });
    }
}
