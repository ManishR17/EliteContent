import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
    selector: 'app-register',
    standalone: true,
    imports: [CommonModule, FormsModule, RouterModule],
    templateUrl: './register.component.html',
    styleUrls: ['./login.component.css'] // Reuse login styles
})
export class RegisterComponent {
    user = {
        full_name: '',
        email: '',
        password: ''
    };
    isLoading = false;
    error = '';

    constructor(private authService: AuthService, private router: Router) { }

    onSubmit() {
        if (!this.user.email || !this.user.password || !this.user.full_name) {
            this.error = 'Please fill in all fields';
            return;
        }

        this.isLoading = true;
        this.error = '';

        this.authService.register(this.user).subscribe({
            next: () => {
                // Auto login after register
                this.authService.login(this.user).subscribe(() => {
                    this.router.navigate(['/dashboard']);
                });
            },
            error: (err) => {
                this.error = err.error?.detail || 'Registration failed';
                this.isLoading = false;
            }
        });
    }
}
