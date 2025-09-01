import"./modulepreload-polyfill-B5Qt9EMX.js";class a{constructor(){this.initializeAuth(),this.initializeEventListeners(),this.loadStats(),this.loadUsers()}async initializeAuth(){try{const e=localStorage.getItem("authenticated"),o=localStorage.getItem("accessToken");if(!e||!o){window.location.href="/login.html";return}const t=await fetch("/auth/check",{method:"GET",headers:{Authorization:`Bearer ${o}`}});if(!t.ok){localStorage.clear(),window.location.href="/login.html";return}const s=await t.json();this.loadUserData(s.user)}catch(e){console.error("Auth check failed:",e),localStorage.clear(),window.location.href="/login.html"}}initializeEventListeners(){document.getElementById("dashboardBtn").addEventListener("click",e=>{e.preventDefault(),window.location.href="/index.html"}),document.getElementById("logoutBtn").addEventListener("click",e=>{e.preventDefault(),this.handleLogout()}),document.getElementById("pastAnalysisBtn").addEventListener("click",e=>{e.preventDefault(),window.location.href="/past-conversations.html"})}loadUserData(e){const o=e.email||"User",t=`${e.first_name||""} ${e.last_name||""}`.trim()||o.split("@")[0],s=t.substring(0,2).toUpperCase();if(document.getElementById("userName").textContent=t,document.getElementById("userAvatar").textContent=s,(e.role||localStorage.getItem("userRole"))!=="admin"){this.showStatus("Access denied. Admin privileges required.","error"),setTimeout(()=>{window.location.href="/index.html"},2e3);return}}async getAccessToken(){const e=localStorage.getItem("accessToken");return e||(window.location.href="/login.html","")}async loadStats(){try{const e=await this.getAccessToken(),o=await fetch("/api/db/users/stats",{method:"GET",headers:{Authorization:`Bearer ${e}`}});if(!o.ok)throw new Error(`HTTP error! status: ${o.status}`);const t=await o.json();if(t.success){const s=t.stats;document.getElementById("totalUsers").textContent=s.total_users,document.getElementById("activeUsers").textContent=s.active_users,document.getElementById("adminUsers").textContent=s.admin_users,document.getElementById("regularUsers").textContent=s.regular_users}else throw new Error(t.error||"Failed to load stats")}catch(e){console.error("Error loading stats:",e),this.showStatus("Error loading statistics: "+e.message,"error")}}async loadUsers(){try{const e=await this.getAccessToken(),o=await fetch("/api/db/users/get_all",{method:"GET",headers:{Authorization:`Bearer ${e}`}});if(!o.ok)throw new Error(`HTTP error! status: ${o.status}`);const t=await o.json();if(t.success)this.renderUsersTable(t.users);else throw new Error(t.error||"Failed to load users")}catch(e){console.error("Error loading users:",e),this.showStatus("Error loading users: "+e.message,"error")}}renderUsersTable(e){const o=document.getElementById("usersTableBody");if(e.length===0){o.innerHTML=`
                        <tr>
                            <td colspan="6" style="text-align: center; padding: 40px;">
                                No users found
                            </td>
                        </tr>
                    `;return}o.innerHTML=e.map(t=>`
                    <tr>
                        <td>
                            <strong>${t.first_name||""} ${t.last_name||""}</strong>
                            ${!t.first_name&&!t.last_name?"<em>No name</em>":""}
                        </td>
                        <td>${t.email}</td>
                        <td>
                            <span class="role-badge role-${t.role}">
                                ${t.role}
                            </span>
                        </td>
                        <td>
                            <span class="status-badge status-${t.is_active?"active":"inactive"}">
                                ${t.is_active?"Active":"Inactive"}
                            </span>
                        </td>
                        <td>
                            ${t.last_login?new Date(t.last_login).toLocaleDateString():"Never"}
                        </td>
                        <td>
                            ${new Date(t.created_at).toLocaleDateString()}
                        </td>

                    </tr>
                `).join("")}showStatus(e,o="success"){const t=document.createElement("div");t.className=`status ${o}`,t.textContent=e,t.style.position="fixed",t.style.top="20px",t.style.right="20px",t.style.zIndex="10000",t.style.display="block",t.style.minWidth="300px",document.body.appendChild(t),setTimeout(()=>{t.remove()},5e3)}async handleLogout(){try{localStorage.removeItem("authenticated"),localStorage.removeItem("userEmail"),localStorage.removeItem("userName"),localStorage.removeItem("accessToken"),window.location.href="/login.html"}catch(e){console.error("Logout failed:",e),window.location.href="/login.html"}}}document.addEventListener("DOMContentLoaded",function(){console.log("DOM loaded, initializing UsersPage"),new a});
