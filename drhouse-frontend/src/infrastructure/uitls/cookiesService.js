
const CookiesService = {
  set: (name, value, days = 7) => {
    const expire = new Date();
    expire.setTime(expire.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expire.toUTCString()};path=/; SameSite=Strict;`;
  },

  get: (name) => {
    const cookies = document.cookie.split('; ').find((item) => item.startsWith(name + '='));
    return cookies ? cookies.split('=')[1] : '';
  },

  remove: (name) => {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/; SameSite=Strict;`;
  },
}

export default CookiesService;
